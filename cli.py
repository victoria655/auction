import bcrypt
from contextlib import contextmanager
from models.db import SessionLocal
from models import User, Item, Bid  # assuming your models are here
from sqlalchemy.orm import Session

@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

class CLI:
    def __init__(self):
        self.logged_in_user = None  # Store User ORM object when logged in

    def run(self):
        self.show_welcome()

    def show_welcome(self):
        while True:
            print("\n" + "="*40)
            print("    🏆 Welcome to the Auction CLI 🏆    ")
            print("="*40)
            print("1. Sign Up (Create New User)")
            print("2. Log In (Returning User)")
            print("3. Exit")
            choice = input("Choose an option (1-3): ").strip()

            if choice == "1":
                self.sign_up()
            elif choice == "2":
                self.log_in()
            elif choice == "3":
                print("===============\n🎉✨ Thank you for stopping by! ✨🎉\n🌈 Until next time... 👋😄")
                break
            else:
                print("Invalid input. Please enter 1, 2, or 3.")

    def sign_up(self):
        print("\n--- Sign Up ---")
        username = input("Enter username: ").strip()
        email = input("Enter email: ").strip()
        password = input("Enter password: ").strip()
        if not username or not email or not password:
            print("All fields are required.")
            return

        with get_session() as session:
            existing = session.query(User).filter(User.username.ilike(username)).first()
            if existing:
                print("Username already exists. Please try logging in.")
                return

            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user = User(username=username, email=email, password=hashed)
            session.add(user)
            session.commit()
            print(f"User '{username}' created successfully. Please log in now.")

    def log_in(self):
        print("\n--- Log In ---")
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()

        with get_session() as session:
            user = session.query(User).filter(User.username.ilike(username)).first()
            if not user:
                print("Username not found. Please sign up first.")
                return

            if self.verify_password(user.password, password):
                print(f"Welcome back, {user.username}!")
                self.logged_in_user = user
                self.user_logged_in_menu()
            else:
                print("Incorrect password. Please try again.")

    def verify_password(self, hashed_pw, password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_pw.encode('utf-8'))

    def user_logged_in_menu(self):
        while True:
            print("\n--- User Menu ---")
            print("1. View Your Bids and Status")
            print("2. View Items and Make a Bid")
            print("3. Upload an Item for Auction")
            print("4. Log Out")
            choice = input("Choose an option (1-4): ").strip()

            if choice == "1":
                self.display_user_bids()
            elif choice == "2":
                self.items_menu_for_user()
            elif choice == "3":
                self.upload_item()
            elif choice == "4":
                print(f"Logging out {self.logged_in_user.username}.")
                self.logged_in_user = None
                break
            else:
                print("Invalid input. Please enter 1, 2, 3, or 4.")

    def display_user_bids(self):
        with get_session() as session:
            bids = session.query(Bid).filter_by(user_id=self.logged_in_user.id).all()
            if not bids:
                print("You have no bids yet.")
                return
            for bid in bids:
                # Assume bid.update_status(session) updates bid.status, expires_at, highest_bid_amount
                bid.update_status(session)

                print(f"\n  \n my bids \n  📦Item: {bid.item.name}  💰Your bid: {bid.amount}   📊 Status: {bid.status}  ⏰Expires at: {bid.expires_at}")
                
                if bid.status == "Lost":
                    print(f"Highest winning bid: {bid.highest_bid_amount}")
                print("-" * 20)

    def items_menu_for_user(self):
        while True:
            self.display_all_items()
            print("\nOptions:")
            print("1. Make a Bid on an Item")
            print("2. Back to User Menu")
            choice = input("Choose an option (1-2): ").strip()
            if choice == "1":
                self.create_bid_for_logged_in_user()
            elif choice == "2":
                break
            else:
                print("Invalid input. Please enter 1 or 2.")

    def display_all_items(self):
        with get_session() as session:
            items = session.query(Item).all()
            if not items:
                print("No items found.")
                return
            print("\nItems:")
            for i in items:
                print(f"ID: {i.id}, Name: {i.name}, Starting Price: {i.starting_price}")

    def create_bid_for_logged_in_user(self):
        with get_session() as session:
            items = session.query(Item).all()
            if not items:
                print("No items available to bid on.")
                return
            try:
                item_id = int(input("Enter the ID of the item you want to bid on: ").strip())
                item = session.query(Item).filter_by(id=item_id).first()
                if not item:
                    print("Item not found.")
                    return
                amount = float(input("Enter your bid amount: ").strip())
                if amount < item.starting_price:
                    print(f"Bid must be at least the starting price: {item.starting_price}")
                    return
            except ValueError:
                print("Please enter valid numeric values.")
                return

            # Create bid and commit
            bid = Bid(amount=amount, user_id=self.logged_in_user.id, item_id=item_id, status="Pending")
            session.add(bid)
            session.commit()
            print(f"Bid of {amount} placed on '{item.name}' successfully.")

    def upload_item(self):
        print("\n--- Upload New Item ---")
        name = input("Enter item name: ").strip()
        description = input("Enter item description: ").strip()
        try:
            starting_price = float(input("Enter starting price: ").strip())
        except ValueError:
            print("Invalid starting price. Please enter a number.")
            return
        
        if not name or not description:
            print("Name and description cannot be empty.")
            return

        with get_session() as session:
            new_item = Item(name=name, description=description,
                            starting_price=starting_price, owner_id=self.logged_in_user.id)
            session.add(new_item)
            session.commit()
            print(f"Item '{name}' uploaded successfully and is now available for bidding.")


if __name__ == "__main__":
    app = CLI()
    app.run()
