#!/usr/bin/env python3
"""
Script to update player_stats_snapshot table using batch API calls
Clears existing snapshot data and fetches fresh data from API
Enhanced with multi-threading support and code/country fields
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
import concurrent.futures
from threading import Lock
import threading

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
        self.request_delay = 1  # Reduced delay between API calls in seconds
        self.max_workers = 4  # Number of concurrent threads
        self.db_lock = Lock()  # Database access lock
        
        # Initialize database schema with new fields
        self._ensure_database_schema()
        
    def _ensure_database_schema(self):
        """Ensure the database has the required schema with code and country fields"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if code column exists
                cursor.execute("PRAGMA table_info(player)")
                columns = [column[1] for column in cursor.fetchall()]
                
                if 'code' not in columns:
                    logger.info("Adding 'code' column to player table")
                    cursor.execute("ALTER TABLE player ADD COLUMN code TEXT")
                    
                if 'country' not in columns:
                    logger.info("Adding 'country' column to player table")
                    cursor.execute("ALTER TABLE player ADD COLUMN country TEXT")
                
                # Create index for code field for faster searching
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_player_code ON player(code)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_player_country ON player(country)")
                
                conn.commit()
                logger.info("Database schema updated successfully")
                
        except Exception as e:
            logger.error(f"Error updating database schema: {e}")
            raise
    
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
            
            # Make API request with timeout
            response = requests.get(api_url, timeout=30)
            
            thread_id = threading.get_ident()
            logger.info(f"[Thread-{thread_id}] API call for {len(pids)} PIDs - Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    return data
                except json.JSONDecodeError as e:
                    logger.error(f"[Thread-{thread_id}] Failed to parse JSON response: {e}")
                    logger.error(f"[Thread-{thread_id}] Response text: {response.text[:500]}...")
                    return None
            else:
                logger.error(f"[Thread-{thread_id}] API request failed with status {response.status_code}")
                logger.error(f"[Thread-{thread_id}] Response: {response.text[:500]}...")
                return None
                
        except requests.exceptions.RequestException as e:
            thread_id = threading.get_ident()
            logger.error(f"[Thread-{thread_id}] API request exception: {e}")
            return None
        except Exception as e:
            thread_id = threading.get_ident()
            logger.error(f"[Thread-{thread_id}] Unexpected error in API call: {e}")
            return None
    
    def process_api_response(self, api_data: Dict, expected_pids: List[str]) -> List[Dict]:
        """Process API response and extract player stats with code and country"""
        processed_players = []
        current_date = date.today().isoformat()
        expected_pids_set = set(str(pid) for pid in expected_pids)
        thread_id = threading.get_ident()
        
        try:
            # The API returns data in format: {"users": [...]}
            if isinstance(api_data, dict) and 'users' in api_data:
                users = api_data['users']
                
                for user_data in users:
                    if isinstance(user_data, dict) and 'pid' in user_data:
                        pid = str(user_data.get('pid', ''))
                        if pid in expected_pids_set:
                            player_info = {
                                'pid': pid,
                                'stat_date': current_date,
                                'versus_rating': user_data.get('versus_rating', 0),
                                'versus_won': user_data.get('versus_won', 0),
                                'versus_plays': user_data.get('versus_plays', 0),
                                'code': user_data.get('code', ''),
                                'country': user_data.get('country', ''),
                                'name': user_data.get('name', '')
                            }
                            processed_players.append(player_info)
                            logger.debug(f"[Thread-{thread_id}] Processed player {pid}: rating={user_data.get('versus_rating', 0)}, country={user_data.get('country', '')}")
            else:
                logger.warning(f"[Thread-{thread_id}] Unexpected API response format: {type(api_data)}")
                if isinstance(api_data, dict):
                    logger.warning(f"[Thread-{thread_id}] Available keys: {list(api_data.keys())}")
            
            logger.info(f"[Thread-{thread_id}] Processed {len(processed_players)} players from API response")
            return processed_players
            
        except Exception as e:
            logger.error(f"[Thread-{thread_id}] Error processing API response: {e}")
            return []
    
    def insert_snapshot_data(self, players_data: List[Dict]):
        """Insert new snapshot data into database with thread safety"""
        if not players_data:
            logger.warning("No player data to insert")
            return
        
        thread_id = threading.get_ident()
        
        try:
            with self.db_lock:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    
                    for player in players_data:
                        # Update player table with code and country if available
                        if player.get('code') or player.get('country') or player.get('name'):
                            cursor.execute("""
                                UPDATE player 
                                SET code = COALESCE(?, code), 
                                    country = COALESCE(?, country),
                                    name = COALESCE(?, name)
                                WHERE pid = ?
                            """, (
                                player.get('code') or None,
                                player.get('country') or None, 
                                player.get('name') or None,
                                player['pid']
                            ))
                        
                        # Insert stats data
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
                    logger.info(f"[Thread-{thread_id}] Successfully inserted {len(players_data)} player stats into database")
                    
        except Exception as e:
            logger.error(f"[Thread-{thread_id}] Error inserting snapshot data: {e}")
            raise
    
    def process_batch(self, batch_pids: List[str], batch_num: int, total_batches: int) -> tuple:
        """Process a single batch of PIDs"""
        thread_id = threading.get_ident()
        logger.info(f"[Thread-{thread_id}] Processing batch {batch_num}/{total_batches} ({len(batch_pids)} PIDs)")
        
        # Call API for this batch
        api_data = self.call_api_batch(batch_pids)
        
        if api_data:
            # Process the response
            processed_players = self.process_api_response(api_data, batch_pids)
            
            if processed_players:
                # Insert into database
                self.insert_snapshot_data(processed_players)
                success_count = len(processed_players)
                logger.info(f"[Thread-{thread_id}] Batch {batch_num} completed successfully: {success_count} players updated")
                return success_count, 0
            else:
                logger.warning(f"[Thread-{thread_id}] Batch {batch_num}: No valid player data processed")
                return 0, len(batch_pids)
        else:
            logger.error(f"[Thread-{thread_id}] Batch {batch_num} failed: API call unsuccessful")
            return 0, len(batch_pids)
    
    def update_all_players(self):
        """Main method to update all player stats using multi-threading"""
        logger.info("Starting player stats update process with multi-threading")
        
        try:
            # Get all PIDs
            all_pids = self.get_all_pids()
            if not all_pids:
                logger.error("No PIDs found in database")
                return False
            
            # Clear existing snapshot data
            self.clear_snapshot_data()
            
            # Create batches
            batches = []
            for i in range(0, len(all_pids), self.batch_size):
                batch_pids = all_pids[i:i + self.batch_size]
                batch_num = (i // self.batch_size) + 1
                batches.append((batch_pids, batch_num))
            
            total_batches = len(batches)
            successful_updates = 0
            failed_updates = 0
            
            logger.info(f"Processing {len(all_pids)} PIDs in {total_batches} batches using {self.max_workers} threads")
            
            # Process batches using ThreadPoolExecutor
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # Submit all batch processing tasks
                future_to_batch = {
                    executor.submit(self.process_batch, batch_pids, batch_num, total_batches): (batch_pids, batch_num)
                    for batch_pids, batch_num in batches
                }
                
                # Collect results as they complete
                for future in concurrent.futures.as_completed(future_to_batch):
                    batch_pids, batch_num = future_to_batch[future]
                    try:
                        success_count, fail_count = future.result()
                        successful_updates += success_count
                        failed_updates += fail_count
                        
                        # Add delay between completion of batches to avoid overwhelming the API
                        time.sleep(self.request_delay)
                        
                    except Exception as e:
                        logger.error(f"Batch {batch_num} generated an exception: {e}")
                        failed_updates += len(batch_pids)
            
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
    
    def search_by_code(self, code: str) -> Optional[Dict]:
        """Search for a player by their code"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT p.pid, p.name, p.code, p.country, 
                           pss.versus_rating, pss.versus_won, pss.versus_plays, pss.stat_date
                    FROM player p
                    LEFT JOIN player_stats_snapshot pss ON p.pid = pss.pid
                    WHERE p.code = ?
                    ORDER BY pss.stat_date DESC
                    LIMIT 1
                """, (code,))
                
                row = cursor.fetchone()
                if row:
                    return {
                        'pid': row[0],
                        'name': row[1], 
                        'code': row[2],
                        'country': row[3],
                        'versus_rating': row[4] or 0,
                        'versus_won': row[5] or 0,
                        'versus_plays': row[6] or 0,
                        'stat_date': row[7]
                    }
                return None
                
        except Exception as e:
            logger.error(f"Error searching by code {code}: {e}")
            return None
    
    def update_country_support(self, countries: List[str] = ['JP', 'HK', 'US']):
        """Update mario_stats.db to support additional countries"""
        try:
            stats_db_path = "mario_stats.db"
            if not os.path.exists(stats_db_path):
                logger.warning(f"mario_stats.db not found at {stats_db_path}")
                return False
                
            with sqlite3.connect(stats_db_path) as conn:
                cursor = conn.cursor()
                
                # Check if country column exists in users table
                cursor.execute("PRAGMA table_info(users)")
                columns = [column[1] for column in cursor.fetchall()]
                
                if 'country' not in columns:
                    logger.info("Adding 'country' column to mario_stats.db users table")
                    cursor.execute("ALTER TABLE users ADD COLUMN country TEXT DEFAULT 'Unknown'")
                    cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_country ON users(country)")
                    conn.commit()
                    logger.info("Successfully added country support to mario_stats.db")
                else:
                    logger.info("Country column already exists in mario_stats.db")
                
                return True
                
        except Exception as e:
            logger.error(f"Error updating country support in mario_stats.db: {e}")
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
                
                # Check how many players have code and country info
                cursor.execute("SELECT COUNT(*) FROM player WHERE code IS NOT NULL AND code != ''")
                code_count = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM player WHERE country IS NOT NULL AND country != ''")
                country_count = cursor.fetchone()[0]
                
                # Get some sample data
                cursor.execute("""
                    SELECT p.pid, p.name, p.code, p.country, pss.versus_rating, pss.versus_won, pss.versus_plays 
                    FROM player p
                    JOIN player_stats_snapshot pss ON p.pid = pss.pid
                    WHERE pss.stat_date = ? 
                    ORDER BY pss.versus_rating DESC 
                    LIMIT 5
                """, (today,))
                sample_data = cursor.fetchall()
                
                logger.info("VERIFICATION RESULTS")
                logger.info("-" * 40)
                logger.info(f"Total players in database: {player_count}")
                logger.info(f"Total snapshot records: {snapshot_count}")
                logger.info(f"Today's snapshot records: {today_count}")
                logger.info(f"Players with code info: {code_count}")
                logger.info(f"Players with country info: {country_count}")
                logger.info(f"Coverage: {(today_count/player_count*100):.1f}%")
                
                if sample_data:
                    logger.info("Top 5 players by rating:")
                    for pid, name, code, country, rating, won, plays in sample_data:
                        logger.info(f"  {name} (PID: {pid[:15]}..., Code: {code or 'N/A'}, Country: {country or 'N/A'}) - Rating: {rating}, Won: {won}, Plays: {plays}")
                
                return today_count > 0
                
        except Exception as e:
            logger.error(f"Error during verification: {e}")
            return False

def main():
    """Main function"""
    logger.info("Starting Mario player stats update with enhanced features")
    
    # Check if database exists
    db_path = "mario_filtered.db"
    if not os.path.exists(db_path):
        logger.error(f"Database file {db_path} not found!")
        sys.exit(1)
    
    try:
        updater = PlayerStatsUpdater(db_path)
        
        # Update country support in mario_stats.db
        logger.info("Updating country support in mario_stats.db...")
        updater.update_country_support(['JP', 'HK', 'US'])
        
        # Perform the update
        success = updater.update_all_players()
        
        if success:
            logger.info("Update process completed successfully")
            
            # Verify the update
            if updater.verify_update():
                logger.info("Verification passed - update was successful!")
                
                # Demonstrate code search functionality
                logger.info("Testing code search functionality...")
                test_result = updater.search_by_code("08VW66RLF")
                if test_result:
                    logger.info(f"Code search test successful: Found {test_result['name']} from {test_result['country']}")
                else:
                    logger.info("Code search test: No result found for test code")
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