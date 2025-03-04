import math


def calculate_monthly_payment(loan_amount, annual_interest_rate, years):
    """
    Calculate the monthly mortgage payment.

    Parameters:
    loan_amount (float): The principal loan amount (e.g., 2500000)
    annual_interest_rate (float): Annual interest rate as a decimal (e.g., 0.08 for 8%)
    years (int or float): Loan term in years

    Returns:
    float: Monthly payment amount
    """
    # Convert annual interest rate to monthly rate
    monthly_interest_rate = annual_interest_rate / 12

    # Calculate total number of payments
    num_payments = 12 * years

    # Calculate monthly payment using the formula:
    # P = (L * r) / (1 - (1 + r)^(-n))
    # Where:
    # P = monthly payment
    # L = loan amount
    # r = monthly interest rate
    # n = total number of payments

    numerator = loan_amount * monthly_interest_rate
    denominator = 1 - math.pow(1 + monthly_interest_rate, -num_payments)

    monthly_payment = numerator / denominator

    return monthly_payment


# Function to calculate total interest paid over the life of the loan
def calculate_total_interest(loan_amount, monthly_payment, years):
    """
    Calculate the total interest paid over the life of the loan.

    Parameters:
    loan_amount (float): The principal loan amount
    monthly_payment (float): The monthly payment amount
    years (int or float): Loan term in years

    Returns:
    float: Total interest paid
    """
    total_paid = monthly_payment * 12 * years
    total_interest = total_paid - loan_amount
    return total_interest


# Function to calculate opportunity cost/investment growth
def calculate_opportunity_cost(payment_diff, years, annual_investment_return):
    """
    Calculate the potential investment value if the monthly payment difference
    was invested at a given return rate.

    Parameters:
    payment_diff (float): Monthly payment difference compared to 30-year mortgage
    years (int): Number of years for investment
    annual_investment_return (float): Annual investment return as a decimal

    Returns:
    float: Total investment value after the period
    """
    monthly_return = annual_investment_return / 12
    months = years * 12

    # Calculate future value of a monthly payment series with growth
    # Formula: PMT * (((1 + r)^n - 1) / r)
    if monthly_return > 0:
        future_value = payment_diff * (
            (pow(1 + monthly_return, months) - 1) / monthly_return
        )
    else:
        future_value = payment_diff * months

    return future_value


# Function to calculate inflation-adjusted value
def calculate_inflation_adjusted_value(value, years, annual_inflation_rate):
    """
    Calculate the present value of a future amount, accounting for inflation.

    Parameters:
    value (float): Future value
    years (int): Number of years
    annual_inflation_rate (float): Annual inflation rate as a decimal

    Returns:
    float: Inflation-adjusted (present) value
    """
    return value / pow(1 + annual_inflation_rate, years)


# Example usage with comparison table
loan_amount = 2500000
annual_interest_rate = 0.08  # 8% annual interest rate assumption
investment_return_rate = 0.4  # 7% annual investment return assumption
annual_inflation_rate = 0.28  # 3% annual inflation rate assumption
monthly_salary = 200000

# Calculate 30-year loan metrics as the baseline for comparison
years_30 = 30
payment_30 = calculate_monthly_payment(loan_amount, annual_interest_rate, years_30)
total_interest_30 = calculate_total_interest(loan_amount, payment_30, years_30)
total_cost_30 = loan_amount + total_interest_30

# Store results for all terms to use in both tables
term_results = []

# Generate results for terms from 1 to 30 years
for term in range(1, 31):
    # Calculate metrics for this term
    monthly_payment = calculate_monthly_payment(loan_amount, annual_interest_rate, term)
    total_interest = calculate_total_interest(loan_amount, monthly_payment, term)
    total_cost = loan_amount + total_interest
    savings = total_cost_30 - total_cost

    # Calculate potential investment value
    # For shorter terms, we invest the difference for the remaining years up to 30
    if term < 30:
        payment_diff = monthly_salary - monthly_payment  # Negative for shorter terms

        if payment_diff < 0:  # For shorter terms where monthly payment is higher than salary
            investment_value_in_term = 0
            remaining_years = 30 - term
            investment_value = calculate_opportunity_cost(
                monthly_salary, remaining_years, investment_return_rate
            )
        else:
            # First investing the higher payment for 'term' years
            investment_value = investment_value_in_term = calculate_opportunity_cost(
                payment_diff, term, investment_return_rate
            )

            # Then investing the full payment for remaining years after loan is paid off
            remaining_years = 30 - term
            investment_value += calculate_opportunity_cost(
                monthly_salary, remaining_years, investment_return_rate
            )
    else:
        investment_value = 0  # No opportunity cost for 30-year term (our baseline)
        investment_value_in_term = 0
    term_results.append(
        {
            "term": term,
            "monthly_payment": monthly_payment,
            "total_interest": total_interest,
            "total_cost": total_cost,
            "savings": savings,
            "investment_value_in_term": investment_value_in_term,
            "investment_value": investment_value,
        }
    )

# Print nominal values table (not adjusted for inflation)
print(f"\nLoan Amount: ${loan_amount:,} at {annual_interest_rate * 100:.1f}% interest")
print(f"Investment Return Assumption: {investment_return_rate * 100:.1f}%")
print("\n=== NOMINAL VALUES (NOT ADJUSTED FOR INFLATION) ===")
print(
    "\n{:<10} {:<18} {:<18} {:<18} {:<18} {:<18} {:<18}".format(
        "Term (Yrs)",
        "Monthly Payment",
        "Total Interest",
        "Total Cost",
        "Savings vs 30yr",
        "Potential Investment (IT)",
        "Potential Investment",
    )
)
print("-" * 103)

for result in term_results:
    print(
        "{:<10} {:>17,.0f} {:>17,.0f} {:>17,.0f} {:>17,.0f} {:>17,.0f} {:>17,.0f}".format(
            result["term"],
            result["monthly_payment"],
            result["total_interest"],
            result["total_cost"],
            result["savings"],
            result["investment_value_in_term"],
            result["investment_value"],
        )
    )

# Print inflation-adjusted values table
print("\n\n=== INFLATION-ADJUSTED VALUES (PRESENT VALUE) ===")
print(f"Inflation Rate Assumption: {annual_inflation_rate * 100:.1f}%")
print(
    "\n{:<10} {:<18} {:<18} {:<18} {:<18} {:<18} {:<18}".format(
        "Term (Yrs)",
        "Monthly Payment",
        "Total Interest",
        "Total Cost",
        "Savings vs 30yr",
        "Potential Investment (IT)",
        "Potential Investment",
    )
)
print("-" * 103)

for result in term_results:
    term = result["term"]

    # For inflation adjustment of the total values, we use the midpoint of the term
    # as a simplification (since payments are made throughout the term)
    midpoint_years = term / 2

    # Adjust for inflation - monthly payment remains the same in nominal terms
    # but decreases in real terms over time
    inflation_adj_total_interest = calculate_inflation_adjusted_value(
        result["total_interest"], midpoint_years, annual_inflation_rate
    )

    inflation_adj_total_cost = loan_amount + inflation_adj_total_interest

    # For savings and investment value, adjust based on the term
    inflation_adj_savings = calculate_inflation_adjusted_value(
        result["savings"], 30, annual_inflation_rate
    )

    inflation_adj_investment_IT = calculate_inflation_adjusted_value(
        result["investment_value_in_term"], 30, annual_inflation_rate
    )

    inflation_adj_investment = calculate_inflation_adjusted_value(
        result["investment_value"], 30, annual_inflation_rate
    )

    print(
        "{:<10} {:>17,.0f} {:>17,.0f} {:>17,.0f} {:>17,.0f} {:>17,.0f} {:>17,.0f}".format(
            term,
            result["monthly_payment"],  # Monthly payment not adjusted for simplicity
            inflation_adj_total_interest,
            inflation_adj_total_cost,
            inflation_adj_savings,
            inflation_adj_investment_IT,
            inflation_adj_investment,
        )
    )
