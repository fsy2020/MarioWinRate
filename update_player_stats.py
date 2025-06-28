#!/usr/bin/env python3
"""
Script to update player_stats_snapshot table using batch API calls
Clears existing snapshot data and fetches fresh data from API
"""

import sqlite3
import requests
import json
import time
import logging
import sys
from datetime import datetime, date
from typing import List, Dict, Optional
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('update_player_stats.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class PlayerStatsUpdater:
    def __init__(self, db_path: str = "mario_filtered.db"):
        self.db_path = db_path
        self.api_base_url = "https://tgrcode.com/mm2/user_info_multiple/"
        self.batch_size = 50  # Number of PIDs to process in one API call
        self.request_delay = 2  # Delay between API calls in seconds
        
    def get_all_pids(self) -> List[str]:
        """Get all PIDs from the player table"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT pid FROM player ORDER BY pid")
                pids = [row[0] for row in cursor.fetchall()]
                logger.info(f"Retrieved {len(pids)} PIDs from database")
                return pids
        except Exception as e:
            logger.error(f"Error retrieving PIDs from database: {e}")
            raise
    
    def clear_snapshot_data(self):
        """Clear all existing data from player_stats_snapshot table"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM player_stats_snapshot")
                deleted_count = cursor.rowcount
                conn.commit()
                logger.info(f"Cleared {deleted_count} records from player_stats_snapshot table")
        except Exception as e:
            logger.error(f"Error clearing snapshot data: {e}")
            raise
    
    def call_api_batch(self, pids: List[str]) -> Optional[Dict]:
        """Call API with batch of PIDs"""
        try:
            # Join PIDs with comma and put them in the URL path
            pid_string = ",".join(pids)
            api_url = f"{self.api_base_url}{pid_string}"
            
            # Make API request
            response = requests.get(api_url, timeout=30)
            
            logger.info(f"API call for {len(pids)} PIDs - Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    return data
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse JSON response: {e}")
                    logger.error(f"Response text: {response.text[:500]}...")
                    return None
            else:
                logger.error(f"API request failed with status {response.status_code}")
                logger.error(f"Response: {response.text[:500]}...")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"API request exception: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in API call: {e}")
            return None
    
    def process_api_response(self, api_data: Dict, expected_pids: List[str]) -> List[Dict]:
        """Process API response and extract player stats"""
        processed_players = []
        current_date = date.today().isoformat()
        expected_pids_set = set(str(pid) for pid in expected_pids)
        
        try:
            # The API returns data in format: {"users": [...]}
            if isinstance(api_data, dict) and 'users' in api_data:
                users = api_data['users']
                
                for user_data in users:
                    if isinstance(user_data, dict) and 'pid' in user_data:
                        pid = str(user_data.get('pid', ''))
                        if pid in expected_pids_set:
                            processed_players.append({
                                'pid': pid,
                                'stat_date': current_date,
                                'versus_rating': user_data.get('versus_rating', 0),
                                'versus_won': user_data.get('versus_won', 0),
                                'versus_plays': user_data.get('versus_plays', 0)
                            })
                            logger.debug(f"Processed player {pid}: rating={user_data.get('versus_rating', 0)}")
            else:
                logger.warning(f"Unexpected API response format: {type(api_data)}")
                if isinstance(api_data, dict):
                    logger.warning(f"Available keys: {list(api_data.keys())}")
            
            logger.info(f"Processed {len(processed_players)} players from API response")
            return processed_players
            
        except Exception as e:
            logger.error(f"Error processing API response: {e}")
            return []
    
    def insert_snapshot_data(self, players_data: List[Dict]):
        """Insert new snapshot data into database"""
        if not players_data:
            logger.warning("No player data to insert")
            return
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                for player in players_data:
                    cursor.execute("""
                        INSERT OR REPLACE INTO player_stats_snapshot 
                        (pid, stat_date, versus_rating, versus_won, versus_plays)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        player['pid'],
                        player['stat_date'],
                        player['versus_rating'],
                        player['versus_won'],
                        player['versus_plays']
                    ))
                
                conn.commit()
                logger.info(f"Successfully inserted {len(players_data)} player stats into database")
                
        except Exception as e:
            logger.error(f"Error inserting snapshot data: {e}")
            raise
    
    def update_all_players(self):
        """Main method to update all player stats"""
        logger.info("Starting player stats update process")
        
        try:
            # Get all PIDs
            all_pids = self.get_all_pids()
            if not all_pids:
                logger.error("No PIDs found in database")
                return False
            
            # Clear existing snapshot data
            self.clear_snapshot_data()
            
            # Process PIDs in batches
            total_batches = (len(all_pids) + self.batch_size - 1) // self.batch_size
            successful_updates = 0
            failed_updates = 0
            
            logger.info(f"Processing {len(all_pids)} PIDs in {total_batches} batches of {self.batch_size}")
            
            for i in range(0, len(all_pids), self.batch_size):
                batch_num = (i // self.batch_size) + 1
                batch_pids = all_pids[i:i + self.batch_size]
                
                logger.info(f"Processing batch {batch_num}/{total_batches} ({len(batch_pids)} PIDs)")
                
                # Call API for this batch
                api_data = self.call_api_batch(batch_pids)
                
                if api_data:
                    # Process the response
                    processed_players = self.process_api_response(api_data, batch_pids)
                    
                    if processed_players:
                        # Insert into database
                        self.insert_snapshot_data(processed_players)
                        successful_updates += len(processed_players)
                        logger.info(f"Batch {batch_num} completed successfully: {len(processed_players)} players updated")
                    else:
                        logger.warning(f"Batch {batch_num}: No valid player data processed")
                        failed_updates += len(batch_pids)
                else:
                    logger.error(f"Batch {batch_num} failed: API call unsuccessful")
                    failed_updates += len(batch_pids)
                
                # Add delay between API calls to avoid rate limiting
                if i + self.batch_size < len(all_pids):  # Don't delay after the last batch
                    logger.info(f"Waiting {self.request_delay} seconds before next batch...")
                    time.sleep(self.request_delay)
            
            # Final statistics
            logger.info("="*60)
            logger.info("UPDATE SUMMARY")
            logger.info("="*60)
            logger.info(f"Total PIDs processed: {len(all_pids)}")
            logger.info(f"Successful updates: {successful_updates}")
            logger.info(f"Failed updates: {failed_updates}")
            logger.info(f"Success rate: {(successful_updates/len(all_pids)*100):.1f}%")
            logger.info("="*60)
            
            return successful_updates > 0
            
        except Exception as e:
            logger.error(f"Critical error during update process: {e}")
            return False
    
    def verify_update(self):
        """Verify the update was successful"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check total records
                cursor.execute("SELECT COUNT(*) FROM player_stats_snapshot")
                snapshot_count = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM player")
                player_count = cursor.fetchone()[0]
                
                # Check today's records
                today = date.today().isoformat()
                cursor.execute("SELECT COUNT(*) FROM player_stats_snapshot WHERE stat_date = ?", (today,))
                today_count = cursor.fetchone()[0]
                
                # Get some sample data
                cursor.execute("""
                    SELECT pid, versus_rating, versus_won, versus_plays 
                    FROM player_stats_snapshot 
                    WHERE stat_date = ? 
                    ORDER BY versus_rating DESC 
                    LIMIT 5
                """, (today,))
                sample_data = cursor.fetchall()
                
                logger.info("VERIFICATION RESULTS")
                logger.info("-" * 40)
                logger.info(f"Total players in database: {player_count}")
                logger.info(f"Total snapshot records: {snapshot_count}")
                logger.info(f"Today's snapshot records: {today_count}")
                logger.info(f"Coverage: {(today_count/player_count*100):.1f}%")
                
                if sample_data:
                    logger.info("Top 5 players by rating:")
                    for pid, rating, won, plays in sample_data:
                        logger.info(f"  PID: {pid[:15]}... Rating: {rating}, Won: {won}, Plays: {plays}")
                
                return today_count > 0
                
        except Exception as e:
            logger.error(f"Error during verification: {e}")
            return False

def main():
    """Main function"""
    logger.info("Starting Mario player stats update")
    
    # Check if database exists
    db_path = "mario_filtered.db"
    if not os.path.exists(db_path):
        logger.error(f"Database file {db_path} not found!")
        sys.exit(1)
    
    try:
        updater = PlayerStatsUpdater(db_path)
        
        # Perform the update
        success = updater.update_all_players()
        
        if success:
            logger.info("Update process completed successfully")
            
            # Verify the update
            if updater.verify_update():
                logger.info("Verification passed - update was successful!")
            else:
                logger.warning("Verification failed - please check the data")
        else:
            logger.error("Update process failed")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("Update process interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 