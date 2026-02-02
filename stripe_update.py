import stripe
import os
import datetime

# TOGGLE THIS: Set to True for live, False for Test
LIVE_MODE = False 

# Pulls key from GitHub Secrets (Use your sk_test_... first!)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def update_subscriptions():
    print(f"Starting Sync. Mode: {'LIVE' if LIVE_MODE else 'TEST'}")
    
    subscriptions = stripe.Subscription.list(status="active", limit=100)

    for sub in subscriptions.auto_paging_iter():
        # 1. Check if they are already on the 1st
        # current_period_end is a Unix timestamp
        end_date = datetime.datetime.fromtimestamp(sub.current_period_end)
        
        if end_date.day == 1:
            print(f"Skipping {sub.id}: Already billed on the 1st.")
            continue

        # 2. Update to the 1st (starting today, Feb 1)
        try:
            if LIVE_MODE:
                stripe.Subscription.modify(
                    sub.id,
                    billing_cycle_anchor="now",
                    # 'always_invoice' with anchor 'now' resets the month starting today.
                    # Note: To avoid ANY proration credit, some users prefer 
                    # clearing 'pending_setup_intent' or using a trial_end of 'now'.
                    proration_behavior="always_invoice" 
                )
                print(f"UPDATED: {sub.id} (Old date was the {end_date.day}th)")
            else:
                print(f"TEST RUN: Would update {sub.id} from the {end_date.day}th to the 1st.")
        
        except Exception as e:
            print(f"Error updating {sub.id}: {e}")

if __name__ == "__main__":
    update_subscriptions()