#!/usr/bin/env python3
"""
Admin Cleanup Script - Remove test/fake reviews easily
"""

import sqlite3
import re

def connect_db():
    """Connect to the SQLite database"""
    try:
        conn = sqlite3.connect('oldweiler.db')
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def find_test_reviews(conn):
    """Find reviews that look like test data"""
    cursor = conn.cursor()
    
    # Common test patterns
    test_patterns = [
        # Test names
        r'test|demo|sample|fake|dummy|example',
        # Test content
        r'test review|sample review|fake review|demo review',
        # Generic content
        r'great work|amazing|excellent|wonderful|fantastic',
        # Very short reviews
        r'^.{1,20}$',
        # Common test phrases
        r'this is a test|testing|test message'
    ]
    
    cursor.execute("SELECT * FROM reviews ORDER BY id DESC")
    all_reviews = cursor.fetchall()
    
    test_reviews = []
    
    for review in all_reviews:
        name = review['name'].lower()
        text = review['text'].lower()
        
        # Check if review matches test patterns
        is_test = False
        for pattern in test_patterns:
            if re.search(pattern, name) or re.search(pattern, text):
                is_test = True
                break
        
        # Also check for very generic content
        if len(text) < 25 and any(word in text for word in ['good', 'great', 'nice', 'amazing']):
            is_test = True
            
        if is_test:
            test_reviews.append(review)
    
    return test_reviews

def show_test_reviews(test_reviews):
    """Display found test reviews"""
    if not test_reviews:
        print("✅ No obvious test reviews found!")
        return
    
    print(f"\n🚨 Found {len(test_reviews)} potential test reviews:")
    print("=" * 80)
    
    for i, review in enumerate(test_reviews, 1):
        print(f"{i}. ID: {review['id']}")
        print(f"   Name: {review['name']}")
        print(f"   Rating: {review['rating'] if review['rating'] else 'N/A'} ⭐")
        print(f"   Text: {review['text'][:100]}{'...' if len(review['text']) > 100 else ''}")
        print(f"   Created: {review['created_at'] if review['created_at'] else 'N/A'}")
        print("-" * 80)

def quick_cleanup(conn):
    """Quick cleanup - remove obvious test reviews"""
    test_reviews = find_test_reviews(conn)
    
    if not test_reviews:
        print("✅ No test reviews to clean up!")
        return
    
    show_test_reviews(test_reviews)
    
    print("\n🗑️ Quick Cleanup Options:")
    print("1. Remove all test reviews automatically")
    print("2. Review each one individually")
    print("3. Cancel")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == '1':
        # Remove all test reviews
        cursor = conn.cursor()
        test_ids = [review['id'] for review in test_reviews]
        
        print(f"\n⚠️  About to delete {len(test_ids)} test reviews:")
        for review in test_reviews:
            print(f"   - {review['name']}: {review['text'][:50]}...")
        
        confirm = input("\nType 'DELETE TESTS' to confirm: ").strip()
        if confirm == 'DELETE TESTS':
            placeholders = ','.join('?' * len(test_ids))
            cursor.execute(f"DELETE FROM reviews WHERE id IN ({placeholders})", test_ids)
            conn.commit()
            print(f"✅ Deleted {len(test_ids)} test reviews!")
        else:
            print("❌ Cleanup cancelled.")
            
    elif choice == '2':
        # Individual review
        individual_cleanup(conn, test_reviews)
    else:
        print("❌ Cleanup cancelled.")

def individual_cleanup(conn, test_reviews):
    """Clean up reviews one by one"""
    cursor = conn.cursor()
    
    for i, review in enumerate(test_reviews, 1):
        print(f"\n📝 Review {i}/{len(test_reviews)}:")
        print(f"ID: {review['id']}")
        print(f"Name: {review['name']}")
        print(f"Text: {review['text']}")
        print(f"Rating: {review['rating'] if review['rating'] else 'N/A'} ⭐")
        
        action = input("\nAction: (d)elete, (k)eep, (s)kip all: ").strip().lower()
        
        if action == 'd':
            cursor.execute("DELETE FROM reviews WHERE id = ?", (review['id'],))
            conn.commit()
            print(f"✅ Deleted review {review['id']}")
        elif action == 's':
            print("⏭️  Skipping remaining reviews...")
            break
        else:
            print("✅ Keeping review")
    
    print("🏁 Individual cleanup complete!")

def main():
    """Main admin cleanup function"""
    print("🧹 ADMIN CLEANUP - Remove Test Reviews")
    print("=" * 50)
    
    conn = connect_db()
    if not conn:
        print("❌ Failed to connect to database")
        return
    
    try:
        while True:
            print("\nOptions:")
            print("1. 🔍 Find test reviews")
            print("2. 🗑️  Quick cleanup (auto-remove)")
            print("3. ✋ Individual cleanup (review each)")
            print("4. 📊 View all reviews")
            print("5. 🗑️  Remove ALL reviews (nuclear option)")
            print("0. Exit")
            
            choice = input("\nEnter choice (0-5): ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                test_reviews = find_test_reviews(conn)
                show_test_reviews(test_reviews)
                if test_reviews:
                    print("\n🗑️  Would you like to clean up these test reviews?")
                    cleanup_choice = input("Enter 'y' for quick cleanup, 'n' to return to menu: ").strip().lower()
                    if cleanup_choice == 'y':
                        quick_cleanup(conn)
            elif choice == '2':
                quick_cleanup(conn)
            elif choice == '3':
                test_reviews = find_test_reviews(conn)
                if test_reviews:
                    individual_cleanup(conn, test_reviews)
                else:
                    print("✅ No test reviews found!")
            elif choice == '4':
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM reviews ORDER BY id DESC")
                reviews = cursor.fetchall()
                print(f"\n📝 Total reviews: {len(reviews)}")
                for review in reviews:
                    print(f"ID: {review['id']} | {review['name']} | {review['text'][:50]}...")
            elif choice == '5':
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM reviews")
                count = cursor.fetchone()[0]
                print(f"\n⚠️  NUCLEAR OPTION: Remove ALL {count} reviews!")
                confirm = input("Type 'NUCLEAR' to confirm: ").strip()
                if confirm == 'NUCLEAR':
                    cursor.execute("DELETE FROM reviews")
                    conn.commit()
                    print(f"💥 All {count} reviews deleted!")
                else:
                    print("❌ Nuclear option cancelled.")
            else:
                print("❌ Invalid choice")
                
            input("\nPress Enter to continue...")
            
    except KeyboardInterrupt:
        print("\n\n👋 Admin cleanup interrupted!")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
