import stripe
import os
import sys
import datetime

# Get and clean the key
raw_key = os.getenv("STRIPE_SECRET_KEY", "")
key = raw_key.strip().replace('"', '').replace("'", "")

if not key:
    print("ERROR: Secret Key is empty.")
    sys.exit(1)

stripe.api_key = key

def update_subscriptions():
    print(f"Starting LIVE Billing Sync at {datetime.datetime.now()}")
    
    try:
        # Fetch active subscriptions
        subscriptions = stripe.Subscription.list(status="active", limit=100)
    except Exception as e:
        print(f"CONNECTION ERROR: {e}")
        sys.exit(1)

    count = 0
    updated_count = 0
    
    # Loop through customers
    for sub in subscriptions.auto_paging_iter():
        count += 1
        
        # SAFETY CHECK: Skip if Paused
        if sub.pause_collection is not None:
            print(f"Skipping {sub.id}: Subscription is PAUSED.")
            continue

        # 1. Check date
        current_end = datetime.datetime.fromtimestamp(sub.current_period_end)
        if current_end.day == 1:
            print(f"Skipping {sub.id}: Already on the 1st.")
            continue

        print(f"Updating {sub.id} (Was day {current_end.day})...")

        try:
            # 2. EXECUTE THE UPDATE
            stripe.Subscription.modify(
                sub.id,
                billing_cycle_anchor="now",
                proration_behavior="none",
                payment_behavior="always_invoice"
            )
            print(f" -> SUCCESS: {sub.id} updated and charged full price.")
            updated_count += 1
            
        except Exception as e:
            print(f" -> FAILED to update {sub.id}: {e}")

    print(f"Job Complete. Scanned {count} subs. Updated {updated_count}.")

if __name__ == "__main__":
    update_subscriptions()