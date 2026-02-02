import stripe
import os
import datetime
import sys

# Get the key from GitHub Secrets
key = os.getenv("STRIPE_SECRET_KEY")

if not key:
    print("ERROR: STRIPE_SECRET_KEY is missing from GitHub Secrets.")
    sys.exit(1)

stripe.api_key = key

def update_subscriptions():
    print(f"Starting Sync at {datetime.datetime.now()}")
    
    try:
        subscriptions = stripe.Subscription.list(status="active", limit=100)
    except Exception as e:
        print(f"FAILED TO CONNECT TO STRIPE: {e}")
        sys.exit(1)

    count = 0
    for sub in subscriptions.auto_paging_iter():
        end_date = datetime.datetime.fromtimestamp(sub.current_period_end)
        
        # Check if already on the 1st
        if end_date.day == 1:
            print(f"Skipping {sub.id}: Already billed on the 1st.")
            continue

        # For now, we only PRINT (Test Mode) so nothing actually happens in Stripe
        print(f"DRY RUN: Would update {sub.id} from day {end_date.day} to the 1st.")
        count += 1

    print(f"Finished. Found {count} subscriptions to update.")

if __name__ == "__main__":
    update_subscriptions()