#!/usr/bin/env python3
"""
Database migration script for Mario Win Rate project
- Modifies player_stats_snapshot table: adds created_at column, removes stat_date
- Creates new player_stats_history table for historical data
- Migrates existing data to new structure
"""

import sqlite3
import os
import sys
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('migration.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class DatabaseMigrator:
    def __init__(self, db_path: str = "mario_filtered.db"):
        self.db_path = db_path
        self.backup_path = f"{db_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
    def create_backup(self):
        """Create a backup of the database before migration"""
        try:
            import shutil
            shutil.copy2(self.db_path, self.backup_path)
            logger.info(f"Database backup created: {self.backup_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
            return False
    
    def check_current_schema(self):
        """Check current database schema"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if player_stats_snapshot table exists
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='player_stats_snapshot'")
                if not cursor.fetchone():
                    logger.error("player_stats_snapshot table not found")
                    return False
                
                # Check current columns
                cursor.execute("PRAGMA table_info(player_stats_snapshot)")
                columns = {row[1]: row[2] for row in cursor.fetchall()}
                
                logger.info("Current player_stats_snapshot schema:")
                for col, type_info in columns.items():
                    logger.info(f"  {col}: {type_info}")
                
                return True
                
        except Exception as e:
            logger.error(f"Error checking schema: {e}")
            return False
    
    def migrate_player_stats_snapshot(self):
        """Migrate player_stats_snapshot table structure"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Step 1: Create new table with updated structure
                logger.info("Creating new player_stats_snapshot table structure...")
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS player_stats_snapshot_new (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        pid TEXT NOT NULL,
                        versus_rating INTEGER NOT NULL DEFAULT 0,
                        versus_won INTEGER NOT NULL DEFAULT 0,
                        versus_plays INTEGER NOT NULL DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (pid) REFERENCES player(pid)
                    )
                """)
                
                # Step 2: Copy data from old table to new table
                logger.info("Migrating existing data...")
                cursor.execute("""
                    INSERT INTO player_stats_snapshot_new (pid, versus_rating, versus_won, versus_plays, created_at)
                    SELECT pid, versus_rating, versus_won, versus_plays, 
                           COALESCE(stat_date || ' 00:00:00', CURRENT_TIMESTAMP) as created_at
                    FROM player_stats_snapshot
                """)
                
                # Step 3: Drop old table and rename new table
                logger.info("Replacing old table with new structure...")
                cursor.execute("DROP TABLE player_stats_snapshot")
                cursor.execute("ALTER TABLE player_stats_snapshot_new RENAME TO player_stats_snapshot")
                
                # Step 4: Create indexes
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_player_stats_snapshot_pid ON player_stats_snapshot(pid)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_player_stats_snapshot_created_at ON player_stats_snapshot(created_at)")
                
                conn.commit()
                logger.info("player_stats_snapshot table migration completed successfully")
                return True
                
        except Exception as e:
            logger.error(f"Error migrating player_stats_snapshot: {e}")
            return False
    
    def create_history_table(self):
        """Create player_stats_history table for historical data"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                logger.info("Creating player_stats_history table...")
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS player_stats_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        pid TEXT NOT NULL,
                        versus_rating INTEGER NOT NULL DEFAULT 0,
                        versus_won INTEGER NOT NULL DEFAULT 0,
                        versus_plays INTEGER NOT NULL DEFAULT 0,
                        win_rate REAL NOT NULL DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (pid) REFERENCES player(pid)
                    )
                """)
                
                # Create indexes for better performance
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_player_stats_history_pid ON player_stats_history(pid)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_player_stats_history_created_at ON player_stats_history(created_at)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_player_stats_history_pid_created_at ON player_stats_history(pid, created_at)")
                
                conn.commit()
                logger.info("player_stats_history table created successfully")
                return True
                
        except Exception as e:
            logger.error(f"Error creating history table: {e}")
            return False
    
    def migrate_existing_data_to_history(self):
        """Migrate existing snapshot data to history table"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                logger.info("Migrating existing data to history table...")
                cursor.execute("""
                    INSERT INTO player_stats_history (pid, versus_rating, versus_won, versus_plays, win_rate, created_at)
                    SELECT pid, versus_rating, versus_won, versus_plays,
                           CASE WHEN versus_plays > 0 THEN (versus_won * 100.0 / versus_plays) ELSE 0 END as win_rate,
                           created_at
                    FROM player_stats_snapshot
                """)
                
                migrated_count = cursor.rowcount
                conn.commit()
                logger.info(f"Migrated {migrated_count} records to history table")
                return True
                
        except Exception as e:
            logger.error(f"Error migrating data to history: {e}")
            return False
    
    def verify_migration(self):
        """Verify the migration was successful"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check new table structure
                cursor.execute("PRAGMA table_info(player_stats_snapshot)")
                snapshot_columns = {row[1]: row[2] for row in cursor.fetchall()}
                
                cursor.execute("PRAGMA table_info(player_stats_history)")
                history_columns = {row[1]: row[2] for row in cursor.fetchall()}
                
                # Check record counts
                cursor.execute("SELECT COUNT(*) FROM player_stats_snapshot")
                snapshot_count = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM player_stats_history")
                history_count = cursor.fetchone()[0]
                
                logger.info("MIGRATION VERIFICATION")
                logger.info("-" * 40)
                logger.info("player_stats_snapshot columns:")
                for col, type_info in snapshot_columns.items():
                    logger.info(f"  {col}: {type_info}")
                
                logger.info("player_stats_history columns:")
                for col, type_info in history_columns.items():
                    logger.info(f"  {col}: {type_info}")
                
                logger.info(f"Snapshot records: {snapshot_count}")
                logger.info(f"History records: {history_count}")
                
                # Verify expected columns exist
                required_snapshot_cols = ['id', 'pid', 'versus_rating', 'versus_won', 'versus_plays', 'created_at']
                required_history_cols = ['id', 'pid', 'versus_rating', 'versus_won', 'versus_plays', 'win_rate', 'created_at']
                
                snapshot_ok = all(col in snapshot_columns for col in required_snapshot_cols)
                history_ok = all(col in history_columns for col in required_history_cols)
                
                # Verify stat_date column is removed
                stat_date_removed = 'stat_date' not in snapshot_columns
                
                if snapshot_ok and history_ok and stat_date_removed:
                    logger.info("✓ Migration verification passed!")
                    return True
                else:
                    logger.error("✗ Migration verification failed!")
                    if not snapshot_ok:
                        logger.error("Missing columns in player_stats_snapshot")
                    if not history_ok:
                        logger.error("Missing columns in player_stats_history")
                    if not stat_date_removed:
                        logger.error("stat_date column still exists in player_stats_snapshot")
                    return False
                    
        except Exception as e:
            logger.error(f"Error during verification: {e}")
            return False
    
    def run_migration(self):
        """Run the complete migration process"""
        logger.info("Starting database migration...")
        
        # Check if database exists
        if not os.path.exists(self.db_path):
            logger.error(f"Database file not found: {self.db_path}")
            return False
        
        # Create backup
        if not self.create_backup():
            logger.error("Failed to create backup. Aborting migration.")
            return False
        
        # Check current schema
        if not self.check_current_schema():
            logger.error("Schema check failed. Aborting migration.")
            return False
        
        # Run migrations
        steps = [
            ("Migrating player_stats_snapshot table", self.migrate_player_stats_snapshot),
            ("Creating player_stats_history table", self.create_history_table),
            ("Migrating data to history table", self.migrate_existing_data_to_history),
            ("Verifying migration", self.verify_migration)
        ]
        
        for step_name, step_func in steps:
            logger.info(f"Step: {step_name}")
            if not step_func():
                logger.error(f"Migration failed at step: {step_name}")
                logger.error(f"Database backup available at: {self.backup_path}")
                return False
        
        logger.info("=" * 50)
        logger.info("DATABASE MIGRATION COMPLETED SUCCESSFULLY!")
        logger.info("=" * 50)
        logger.info(f"Backup created: {self.backup_path}")
        logger.info("You can now run the updated application with the new schema.")
        return True

def main():
    """Main function to run the migration"""
    if len(sys.argv) > 1:
        db_path = sys.argv[1]
    else:
        db_path = "mario_filtered.db"
    
    migrator = DatabaseMigrator(db_path)
    success = migrator.run_migration()
    
    if success:
        logger.info("Migration completed successfully!")
        sys.exit(0)
    else:
        logger.error("Migration failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 