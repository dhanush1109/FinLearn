from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = '\x1eh\xfa\xdat\x18)\x1e3<\x8d\xe6\xe8J\xb3io\x11\xe9\x17\x00\xa7V\xca'

# Global variables to store player score and money
player_score = 0
player_money = 1000

@app.route('/')
def start():
    return render_template('start.html')

@app.route('/instructions')
def instructions():
    return render_template('instructions.html')

@app.route('/regions')
def regions():
    return render_template('regions.html')

@app.before_request
def initialize_game():
    if 'player_money' not in session:
        session['player_money'] = 1000
    if 'player_score' not in session:
        session['player_score'] = 0
    if 'challenge_number' not in session:
        session['challenge_number'] = 1

# Route for Region 1: Valley of Ventures
@app.route('/region1', methods=['GET', 'POST'])
def region1():
    return render_template('region1.html', player_money=session['player_money'], player_score=session['player_score'])

# Challenge 1: Stock Opportunity (Region 1)
@app.route('/region1/challenge1', methods=['GET', 'POST'])
def region1_challenge1():
    if request.method == 'POST':
        investment_choice = request.form['investment_choice']
        # Handle Challenge 1: Stock Opportunity
        if investment_choice == 'a':
            session['player_money'] += 37.5  # 15% return on $250
            session['player_score'] += 10  # Points for high-risk, high-return investment
        elif investment_choice == 'b':
            session['player_money'] += 0  # No gain or loss on $500
            session['player_score'] += 5  # Points for moderate risk, no return
        elif investment_choice == 'c':
            session['player_money'] += 67.5  # 10% return on $150 (Tech) + 5% on $350 (Bonds)
            session['player_score'] += 15  # Points for diversification (lower risk)

        # Move to Challenge 2
        session['challenge_number'] = 2
        return redirect(url_for('region1_challenge2'))

    return render_template('region1_challenge1.html', player_money=session['player_money'], player_score=session['player_score'])

# Challenge 2: Gold vs. Real Estate (Region 1)
@app.route('/region1/challenge2', methods=['GET', 'POST'])
def region1_challenge2():
    if request.method == 'POST':
        investment_choice = request.form['investment_choice']
        # Handle Challenge 2: Gold vs. Real Estate
        if investment_choice == 'a':
            session['player_money'] += 40  # 8% return on $500 for gold
            session['player_score'] += 10  # Points for short-term investment
        elif investment_choice == 'b':
            session['player_money'] += 75  # 15% return on $500 for real estate after 3 years
            session['player_score'] += 20  # Points for long-term growth investment
        elif investment_choice == 'c':
            session['player_money'] += 57.5  # Gold +8% on $250, Real Estate +15% on $250
            session['player_score'] += 15  # Points for balanced investment

        # Move to Region 2
        return redirect(url_for('region2'))

    return render_template('region1_challenge2.html', player_money=session['player_money'], player_score=session['player_score'])

# Route for Region 2: Forest of Finance
@app.route('/region2', methods=['GET', 'POST'])
def region2():
    return render_template('region2.html', player_money=session['player_money'], player_score=session['player_score'])

# Challenge 1: Emergency Expense (Region 2)
@app.route('/region2/challenge1', methods=['GET', 'POST'])
def region2_challenge1():
    if request.method == 'POST':
        expense_choice = request.form['expense_choice']
        # Handle Challenge 1: Emergency Expense
        if expense_choice == 'a':
            session['player_money'] -= 200  # Investment decreased temporarily
            session['player_score'] += 10  # Points for tough decision to delay investment
        elif expense_choice == 'b':
            session['player_money'] -= 200  # Savings decreased
            session['player_score'] += 15  # Points for using savings (avoiding debt)
        elif expense_choice == 'c':
            session['player_money'] -= 220  # Debt incurs 10% interest
            session['player_score'] -= 5  # Points for borrowing and facing interest

        # Move to Challenge 2
        session['challenge_number'] = 2
        return redirect(url_for('region2_challenge2'))

    return render_template('region2_challenge1.html', player_money=session['player_money'], player_score=session['player_score'])

# Challenge 2: Luxury Temptation (Region 2)
@app.route('/region2/challenge2', methods=['GET', 'POST'])
def region2_challenge2():
    if request.method == 'POST':
        expense_choice = request.form['expense_choice']
        # Handle Challenge 2: Luxury Temptation
        if expense_choice == 'a':
            session['player_money'] -= 200  # Immediate loss for luxury purchase
            session['player_score'] -= 5  # Points for impulsive spending
        elif expense_choice == 'b':
            session['player_money']  # No change in portfolio
            session['player_score'] += 10  # Points for avoiding impulsive buying
        elif expense_choice == 'c':
            session['player_money'] += 220  # Gain from resale after 3 turns
            session['player_score'] += 20  # Points for making a wise purchase

        # Move to Region 3
        return redirect(url_for('region3'))

    return render_template('region2_challenge2.html', player_money=session['player_money'], player_score=session['player_score'])

# Route for Region 3: Canyon of Compounders
@app.route('/region3', methods=['GET', 'POST'])
def region3():
    return render_template('region3.html', player_money=session['player_money'], player_score=session['player_score'])

# Challenge 1: Reinvestment Decision (Region 3)
@app.route('/region3/challenge1', methods=['GET', 'POST'])
def region3_challenge1():
    if request.method == 'POST':
        reinvest_choice = request.form['reinvest_choice']
        # Handle Challenge 1: Reinvestment Decision
        if reinvest_choice == 'a':
            session['player_money'] -= 50  # Immediate consumption
            session['player_score'] -= 5  # Points deducted for poor financial decision
        elif reinvest_choice == 'b':
            session['player_money'] += 10  # $60 growth - $50 initial
            session['player_score'] += 20  # High points for wise reinvestment
        elif reinvest_choice == 'c':
            session['player_money'] += 1  # $51 growth - $50 initial
            session['player_score'] += 10  # Moderate points for cautious saving

        # Move to Challenge 2
        session['challenge_number'] = 2
        return redirect(url_for('region3_challenge2'))

    return render_template(
        'region3_challenge1.html', 
        player_money=session['player_money'], 
        player_score=session['player_score']
    )


# Challenge 2: Long-Term vs Short-Term Gains (Region 3)
@app.route('/region3/challenge2', methods=['GET', 'POST'])
def region3_challenge2():
    if request.method == 'POST':
        gains_choice = request.form['gains_choice']
        # Handle Challenge 2: Long-Term vs Short-Term Gains
        if gains_choice == 'a':
            session['player_money'] += 50  # Short-term gain
            session['player_score'] += 5  # Fewer points for quick returns
        elif gains_choice == 'b':
            session['player_money'] += 100  # Long-term gain
            session['player_score'] += 20  # High points for patience and long-term thinking
        elif gains_choice == 'c':
            session['player_money'] += 100  # Gain split: $50 immediate + $50 later
            session['player_score'] += 10  # Moderate points for balanced choice

        # Move to Region 4
        return redirect(url_for('region4')) # Replace with next region or summary endpoint

    return render_template(
        'region3_challenge2.html', 
        player_money=session['player_money'], 
        player_score=session['player_score']
    )

# Route for Region 4: City of Cycles
@app.route('/region4', methods=['GET', 'POST'])
def region4():
    return render_template('region4.html', player_money=session['player_money'], player_score=session['player_score'])

# Challenge 1: Market Timing (Region 4)
@app.route('/region4/challenge1', methods=['GET', 'POST'])
def region4_challenge1():
    if request.method == 'POST':
        market_choice = request.form['market_choice']
        # Handle Challenge 1: Market Timing
        if market_choice == 'a':
            session['player_money'] -= 450  # Loss due to short-term market volatility
            session['player_score'] -= 10  # Negative points for risky behavior
        elif market_choice == 'b':
            session['player_money']  # No immediate change, but missed opportunity
            session['player_score'] -= 5  # Minor penalty for indecision
        elif market_choice == 'c':
            session['player_money'] -= 50  # Loss minimized through dollar-cost averaging
            session['player_score'] += 15  # Positive points for risk management

        # Move to Challenge 2
        session['challenge_number'] = 2
        return redirect(url_for('region4_challenge2'))

    return render_template(
        'region4_challenge1.html', 
        player_money=session['player_money'], 
        player_score=session['player_score']
    )


# Challenge 2: Recession Warning (Region 4)
@app.route('/region4/challenge2', methods=['GET', 'POST'])
def region4_challenge2():
    if request.method == 'POST':
        recession_choice = request.form['recession_choice']
        # Handle Challenge 2: Recession Warning
        if recession_choice == 'a':
            session['player_money'] -= 30  # Limited loss due to safer assets
            session['player_score'] += 15  # High points for prudent decision
        elif recession_choice == 'b':
            session['player_money'] -= 200  # Large loss from market exposure
            session['player_score'] -= 10  # Negative points for inaction
        elif recession_choice == 'c':
            session['player_money']  # No loss, but opportunity cost
            session['player_score'] += 5  # Moderate points for playing it safe

        # Move to Region 5
        session['challenge_number'] = None
        return redirect(url_for('region5')) # Replace with next region or summary endpoint
    
    return render_template(
        'region4_challenge2.html', 
        player_money=session['player_money'], 
        player_score=session['player_score']
    )

@app.route('/region5', methods=['GET', 'POST'])
def region5():
    return render_template('region5.html', player_money=session['player_money'], player_score=session['player_score'])

# Challenge 1: Retirement Planning (Region 5)
@app.route('/region5/challenge1', methods=['GET', 'POST'])
def region5_challenge1():
    if request.method == 'POST':
        retirement_choice = request.form['retirement_choice']
        # Handle Challenge 1: Retirement Planning
        if retirement_choice == 'a':
            session['player_money'] -= 50  # Contribute small amount now
            session['player_score'] += 15  # Positive points for prudent planning
            session['retirement_fund'] = session.get('retirement_fund', 0) + 52.5  # Gradual growth
        elif retirement_choice == 'b':
            session['player_money']  # No immediate impact
            session['player_score'] -= 5  # Negative points for missed opportunity
        elif retirement_choice == 'c':
            session['player_money'] -= 500  # Large contribution impacts liquidity
            session['player_score'] += 25  # High points for long-term commitment
            session['retirement_fund'] = session.get('retirement_fund', 0) + 550  # Significant growth

        # Move to Challenge 2
        session['challenge_number'] = 2
        return redirect(url_for('region5_challenge2'))

    return render_template(
        'region5_challenge1.html', 
        player_money=session['player_money'], 
        player_score=session['player_score'], 
        retirement_fund=session.get('retirement_fund', 0)
    )


# Challenge 2: Life Insurance (Region 5)
@app.route('/region5/challenge2', methods=['GET', 'POST'])
def region5_challenge2():
    if request.method == 'POST':
        insurance_choice = request.form['insurance_choice']
        # Handle Challenge 2: Life Insurance
        if insurance_choice == 'a':
            session['player_money'] -= 100  # Cost of the premium
            session['player_score'] += 20  # Positive points for risk management
        elif insurance_choice == 'b':
            session['player_money']  # No immediate impact
            session['player_score'] -= 10  # Negative points for taking a risk
        elif insurance_choice == 'c':
            session['player_money'] -= 100  # Cost of the plan
            session['player_score'] += 25  # High points for combining insurance with investment
            session['player_money'] *= 1.05  # Portfolio grows by 5%

        # End of Region 5 - Move to Final Stage or Summary
        return redirect(url_for('golden_portfolio_test'))  # Replace with the next stage of the game

    return render_template(
        'region5_challenge2.html', 
        player_money=session['player_money'], 
        player_score=session['player_score']
    )

# Golden Portfolio Test (Final Question)
@app.route('/golden_portfolio_test', methods=['GET', 'POST'])
def golden_portfolio_test():
    if request.method == 'POST':
        final_answer = request.form['final_answer']
        # Handle Final Question
        if final_answer == 'b':
            session['player_score'] += 20  # Bonus points for correct answer
            message = "Correct! Compound interest helps your investments grow exponentially."
        else:
            session['player_score'] -= 10  # Penalty for incorrect answer
            message = "Incorrect. The correct answer is (b): It allows your investment to grow exponentially."

        # Redirect to summary page
        session['final_message'] = message
        return redirect(url_for('game_summary'))

    return render_template(
        'golden_portfolio_test.html', 
        player_money=session['player_money'], 
        player_score=session['player_score']
    )

# Game Summary Page
@app.route('/game_summary', methods=['GET'])
def game_summary():
    final_message = session.get('final_message', "Your journey is complete!")
    return render_template(
        'game_summary.html', 
        player_money=session['player_money'], 
        player_score=session['player_score'], 
        final_message=final_message
    )

# End Game Page
@app.route('/end_game', methods=['GET'])
def end_game():
    return render_template('end_game.html')

if __name__ == '__main__':
    app.run()
