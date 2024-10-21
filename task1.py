import streamlit as st

class ATM:
    def __init__(self, initial_balance=1000):
        """
        Initializes an ATM instance with a default balance, empty transaction history,
        and a default PIN of '1234'.
        """
        self.balance = initial_balance
        self.pin = '1234'
        self.transaction_history = []

    def check_balance(self):
        """
        Returns the current account balance.
        """
        self.transaction_history.append(f"Checked balance: ${self.balance:.2f}")
        return f"Your current balance is: ${self.balance:.2f}"

    def deposit(self, amount):
        """
        Deposits the specified amount to the user's account.
        """
        if amount > 0:
            self.balance += amount
            self.transaction_history.append(f"Deposited: ${amount:.2f}")
            return f"${amount:.2f} deposited successfully."
        return "Invalid deposit amount."

    def withdraw(self, amount):
        """
        Withdraws the specified amount from the user's account, if sufficient balance exists.
        """
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.transaction_history.append(f"Withdrew: ${amount:.2f}")
            return f"${amount:.2f} withdrawn successfully."
        return "Insufficient funds or invalid amount."

    def change_pin(self, new_pin):
        """
        Changes the user's PIN.
        """
        if len(new_pin) == 4 and new_pin.isdigit():
            self.pin = new_pin
            self.transaction_history.append("Changed PIN")
            return "PIN changed successfully."
        return "Invalid PIN format. Please enter a 4-digit number."

    def show_transaction_history(self):
        """
        Returns the transaction history for the user.
        """
        if not self.transaction_history:
            return "No transactions available."
        return "\n".join([f"- {transaction}" for transaction in self.transaction_history])


# Streamlit Frontend
def atm_app():
    if 'atm' not in st.session_state:
        # Store the ATM instance in session state to persist balance and history
        st.session_state.atm = ATM()

    atm = st.session_state.atm  # Access ATM instance from session state
    
    st.title("ATM Machine Simulation")

    # Session state to store the PIN and ATM instance
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.pin_attempts = 0

    # Authenticate User PIN
    if not st.session_state.authenticated:
        st.subheader("Please enter your PIN to continue:")
        entered_pin = st.text_input("PIN:", type="password")
        
        if st.button("Submit PIN"):
            if entered_pin == atm.pin:
                st.session_state.authenticated = True
                st.success("Authentication successful!")
            else:
                st.session_state.pin_attempts += 1
                st.error(f"Incorrect PIN. Attempt {st.session_state.pin_attempts}/3")
                if st.session_state.pin_attempts >= 3:
                    st.error("Too many incorrect attempts. Exiting.")
                    st.stop()  # Stop execution if too many incorrect attempts
    else:
        # Main Menu for authenticated users
        st.sidebar.title("ATM Menu")
        menu = st.sidebar.selectbox("Choose an option:", ("Balance Inquiry", "Cash Withdrawal", "Cash Deposit", "Change PIN", "Transaction History", "Logout"))

        if menu == "Balance Inquiry":
            st.subheader("Balance Inquiry")
            st.write(atm.check_balance())

        elif menu == "Cash Withdrawal":
            st.subheader("Cash Withdrawal")
            withdrawal_amount = st.number_input("Enter amount to withdraw:", min_value=1, step=1)
            if st.button("Withdraw"):
                result = atm.withdraw(withdrawal_amount)
                st.write(result)

        elif menu == "Cash Deposit":
            st.subheader("Cash Deposit")
            deposit_amount = st.number_input("Enter amount to deposit:", min_value=1, step=1)
            if st.button("Deposit"):
                result = atm.deposit(deposit_amount)
                st.write(result)

        elif menu == "Change PIN":
            st.subheader("Change PIN")
            new_pin = st.text_input("Enter your new 4-digit PIN:", type="password")
            if st.button("Change PIN"):
                result = atm.change_pin(new_pin)
                st.write(result)

        elif menu == "Transaction History":
            st.subheader("Transaction History")
            history = atm.show_transaction_history()
            st.text(history)

        elif menu == "Logout":
            st.session_state.authenticated = False
            st.session_state.pin_attempts = 0
            st.write("You have been logged out. Refresh the page to login again.")

# Run the app
if __name__ == "__main__":
    atm_app()
