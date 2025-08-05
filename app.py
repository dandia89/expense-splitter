import streamlit as st
import pandas as pd

def parse_expenses(expense_string):
    try:
        if 'owe:' in expense_string.lower():
            expense_parts = expense_string.lower().split('owe:')
            if len(expense_parts) < 2:
                return 0, []
            expense_string = expense_parts[1].strip()

        expenses = expense_string.strip().split('+')
        total = 0
        expense_items = []

        for expense in expenses:
            expense = expense.strip()
            amount = ''.join(c for c in expense if c.isdigit() or c == '.')
            description = expense[expense.find('('):].strip('() ') if '(' in expense else ''

            if amount:
                amount_float = float(amount)
                total += amount_float
                expense_items.append({'description': description, 'amount': amount_float})

        return total, expense_items
    except:
        return 0, []

def calculate_split(f_expenses, asad_expenses):
    total_f, f_items = parse_expenses(f_expenses)
    total_asad, asad_items = parse_expenses(asad_expenses)
    net_difference = total_asad - total_f
    return {
        'asad_owes': total_asad,
        'f_owes': total_f,
        'net_difference': net_difference,
        'asad_items': asad_items,
        'f_items': f_items
    }

def main():
    st.title("Expense Splitter: F & Asad")

    f_input = st.text_area("Paste F's Expenses (include 'F owe:')", height=150)
    asad_input = st.text_area("Paste Asad's Expenses (include 'Asad owe:')", height=150)

    if st.button("Calculate"):
        result = calculate_split(f_input, asad_input)

        st.subheader("Results")
        st.write(f"F owes Asad: ${result['f_owes']:.2f}")
        st.write(f"Asad owes F: ${result['asad_owes']:.2f}")

        if result['net_difference'] > 0:
            st.success(f"Final: Asad pays F ${result['net_difference']:.2f}")
        elif result['net_difference'] < 0:
            st.success(f"Final: F pays Asad ${abs(result['net_difference']):.2f}")
        else:
            st.info("No payment needed. You're even!")

        # Show tables
        if result['f_items']:
            st.markdown("### F's Expenses")
            st.dataframe(pd.DataFrame(result['f_items']))

        if result['asad_items']:
            st.markdown("### Asad's Expenses")
            st.dataframe(pd.DataFrame(result['asad_items']))

if __name__ == "__main__":
    main()
