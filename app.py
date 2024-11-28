from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = '\x1eh\xfa\xdat\x18)\x1e3<\x8d\xe6\xe8J\xb3io\x11\xe9\x17\x00\xa7V\xca'

# Global variables
player_money = 1000
player_score = 0
challenge_number = 1

@app.before_request
def initialize_game():
    global player_money, player_score, challenge_number

    if challenge_number == 1:  # Initialize if it's the start of the game
        player_money = 1000
        player_score = 0
        challenge_number = 1

@app.route('/')
def start():
    return render_template('start.html')

@app.route('/instructions')
def instructions():
    return render_template('instructions.html')

@app.route('/regions')
def regions():
    return render_template('regions.html')

# Route for Region 1: Valley of Ventures
@app.route('/region1', methods=['GET', 'POST'])
def region1():
    return render_template('region1.html', player_money=player_money, player_score=player_score)

# Challenge 1: Stock Opportunity (Region 1)
@app.route('/region1/challenge1', methods=['GET', 'POST'])
def region1_challenge1():
    global player_money, player_score, challenge_number

    if request.method == 'POST':
        investment_choice = request.form['investment_choice']

        # Handle Challenge 1: Stock Opportunity
        if investment_choice == 'a':
            player_money += 37.5  # 15% return on $250
            player_score += 10  # Points for high-risk, high-return investment
        elif investment_choice == 'b':
            player_money = 25  # No gain or loss on $500
            player_score += 5  # Points for moderate risk, no return
        elif investment_choice == 'c':
            player_money += 67.5  # 10% return on $150 (Tech) + 5% on $350 (Bonds)
            player_score += 15  # Points for diversification (lower risk)

        # Move to Challenge 2
        challenge_number = 2
        return redirect(url_for('region1_challenge2'))

    return render_template('region1_challenge1.html', player_money=player_money, player_score=player_score)


# Challenge 2: Gold vs. Real Estate (Region 1)
@app.route('/region1/challenge2', methods=['GET', 'POST'])
def region1_challenge2():
    global player_money, player_score

    if request.method == 'POST':
        investment_choice = request.form['investment_choice']

        # Handle Challenge 2: Gold vs. Real Estate
        if investment_choice == 'a':
            player_money += 40  # 8% return on $500 for gold
            player_score += 10  # Points for short-term investment
        elif investment_choice == 'b':
            player_money += 75  # 15% return on $500 for real estate after 3 years
            player_score += 20  # Points for long-term growth investment
        elif investment_choice == 'c':
            player_money += 57.5  # Gold +8% on $250, Real Estate +15% on $250
            player_score += 15  # Points for balanced investment

        # Move to Region 2 or another part of the game
        return redirect(url_for('region2'))  # Placeholder for next region

    return render_template('region1_challenge2.html', player_money=player_money, player_score=player_score)

# Route for Region 2: Forest of Finance
@app.route('/region2', methods=['GET', 'POST'])
def region2():
    return render_template('region2.html', player_money=player_money, player_score=player_score)

# Challenge 1: Emergency Expense (Region 2)
@app.route('/region2/challenge1', methods=['GET', 'POST'])
def region2_challenge1():
    global player_money, player_score

    if request.method == 'POST':
        expense_choice = request.form['expense_choice']
        # Handle Challenge 1: Emergency Expense
        if expense_choice == 'a':
            player_money -= 200  # Investment decreased temporarily
            player_score += 10  # Points for tough decision to delay investment
        elif expense_choice == 'b':
            player_money -= 200  # Savings decreased
            player_score += 15  # Points for using savings (avoiding debt)
        elif expense_choice == 'c':
            player_money -= 220  # Debt incurs 10% interest
            player_score -= 5  # Points for borrowing and facing interest

        # Move to Challenge 2
        challenge_number = 2
        return redirect(url_for('region2_challenge2'))

    return render_template('region2_challenge1.html', player_money=player_money, player_score=player_score)

# Challenge 2: Luxury Temptation (Region 2)
@app.route('/region2/challenge2', methods=['GET', 'POST'])
def region2_challenge2():
    global player_money, player_score

    if request.method == 'POST':
        expense_choice = request.form['expense_choice']
        # Handle Challenge 2: Luxury Temptation
        if expense_choice == 'a':
            player_money -= 200  # Immediate loss for luxury purchase
            player_score -= 5  # Points for impulsive spending
        elif expense_choice == 'b':
            player_money  # No change in portfolio
            player_score += 10  # Points for avoiding impulsive buying
        elif expense_choice == 'c':
            player_money += 220  # Gain from resale after 3 turns
            player_score += 20  # Points for making a wise purchase

        # Move to Region 3
        return redirect(url_for('region3'))

    return render_template('region2_challenge2.html', player_money=player_money, player_score=player_score)

# Route for Region 3: Canyon of Compounders
@app.route('/region3', methods=['GET', 'POST'])
def region3():
    return render_template('region3.html', player_money=player_money, player_score=player_score)

# Challenge 1: Reinvestment Decision (Region 3)
@app.route('/region3/challenge1', methods=['GET', 'POST'])
def region3_challenge1():
    global player_money, player_score

    if request.method == 'POST':
        reinvest_choice = request.form['reinvest_choice']
        # Handle Challenge 1: Reinvestment Decision
        if reinvest_choice == 'a':
            player_money -= 50  # Immediate consumption
            player_score -= 5  # Points deducted for poor financial decision
        elif reinvest_choice == 'b':
            player_money += 75  # $60 growth - $50 initial
            player_score += 20  # High points for wise reinvestment
        elif reinvest_choice == 'c':
            player_money += 50  # $51 growth - $50 initial
            player_score += 10  # Moderate points for cautious saving

        # Move to Challenge 2
        challenge_number = 2
        return redirect(url_for('region3_challenge2'))

    return render_template(
        'region3_challenge1.html', 
        player_money=player_money, 
        player_score=player_score
    )

# Challenge 2: Long-Term vs Short-Term Gains (Region 3)
@app.route('/region3/challenge2', methods=['GET', 'POST'])
def region3_challenge2():
    global player_money, player_score

    if request.method == 'POST':
        gains_choice = request.form['gains_choice']
        # Handle Challenge 2: Long-Term vs Short-Term Gains
        if gains_choice == 'a':
            player_money += 50  # Short-term gain
            player_score += 5  # Fewer points for quick returns
        elif gains_choice == 'b':
            player_money += 100  # Long-term gain
            player_score += 20  # High points for patience and long-term thinking
        elif gains_choice == 'c':
            player_money += 80  # Gain split: $50 immediate + $50 later
            player_score += 10  # Moderate points for balanced choice

        # Move to Region 4
        return redirect(url_for('region4')) # Replace with next region or summary endpoint

    return render_template(
        'region3_challenge2.html', 
        player_money=player_money, 
        player_score=player_score
    )

# Route for Region 4: City of Cycles
@app.route('/region4', methods=['GET', 'POST'])
def region4():
    return render_template('region4.html', player_money=player_money, player_score=player_score)

# Challenge 1: Market Timing (Region 4)
@app.route('/region4/challenge1', methods=['GET', 'POST'])
def region4_challenge1():
    global player_money, player_score

    if request.method == 'POST':
        market_choice = request.form['market_choice']
        # Handle Challenge 1: Market Timing
        if market_choice == 'a':
            player_money -= 450  # Loss due to short-term market volatility
            player_score -= 10  # Negative points for risky behavior
        elif market_choice == 'b':
            player_money  # No immediate change, but missed opportunity
            player_score -= 5  # Minor penalty for indecision
        elif market_choice == 'c':
            player_money += 650  # Large gain after market correction
            player_score += 30  # Big points for understanding market cycles

        # Move to Region 5
        return redirect(url_for('region5')) # Next region

    return render_template('region4_challenge1.html', player_money=player_money, player_score=player_score)

# Challenge 2: Retirement Planning (Region 4)
@app.route('/region4/challenge2', methods=['GET', 'POST'])
def region4_challenge2():
    global player_money, player_score

    if request.method == 'POST':
        plan_choice = request.form['plan_choice']
        # Handle Challenge 2: Retirement Planning
        if plan_choice == 'a':
            player_money += 200  # Money saved for retirement
            player_score += 15  # Points for early retirement planning
        elif plan_choice == 'b':
            player_money += 150  # Small contributions over time
            player_score += 10  # Points for consistent contributions
        elif plan_choice == 'c':
            player_money -= 90  # Immediate expense, missed retirement opportunity
            player_score -= 5  # Points deducted for missing out on long-term planning

        # End of game (or next phase)
        return redirect(url_for('game_summary'))  # Replace with final summary endpoint

    return render_template('region4_challenge2.html', player_money=player_money, player_score=player_score)

# Route for Region 5: Summit of Savvy Investors
@app.route('/region5', methods=['GET', 'POST'])
def region5():
    return render_template('region5.html', player_money=player_money, player_score=player_score)

# Challenge 1: Investment in Bonds (Region 5)
@app.route('/region5/challenge1', methods=['GET', 'POST'])
def region5_challenge1():
    global player_money, player_score

    if request.method == 'POST':
        bond_choice = request.form['bond_choice']
        # Handle Challenge 1: Investment in Bonds
        if bond_choice == 'a':
            player_money += 300  # Bonds earn steady returns
            player_score += 15  # Points for playing it safe
        elif bond_choice == 'b':
            player_money -= 100  # Market volatility affects bond price
            player_score -= 5  # Points deducted for market risk
        elif bond_choice == 'c':
            player_money += 500  # Long-term bond investment pays off
            player_score += 20  # Points for long-term strategy

        # Move to Challenge 2
        challenge_number = 2
        return redirect(url_for('region5_challenge2'))

    return render_template('region5_challenge1.html', player_money=player_money, player_score=player_score)

# Challenge 2: Crypto vs. Traditional Investments (Region 5)
@app.route('/region5/challenge2', methods=['GET', 'POST'])
def region5_challenge2():
    global player_money, player_score

    if request.method == 'POST':
        investment_choice = request.form['investment_choice']
        # Handle Challenge 2: Crypto vs. Traditional Investments
        if investment_choice == 'a':
            player_money += 400  # Crypto boom rewards early investors
            player_score += 25  # Points for risk-taking in high-growth assets
        elif investment_choice == 'b':
            player_money += 250  # Traditional investments grow steadily
            player_score += 15  # Points for safe investments
        elif investment_choice == 'c':
            player_money += 350  # Balanced approach gains from both markets
            player_score += 20  # Points for diversification

        # Move to final challenge or summary
        return redirect(url_for('game_summary'))

    return render_template('region5_challenge2.html', player_money=player_money, player_score=player_score)

# Game Summary Page
@app.route('/game_summary', methods=['GET'])
def game_summary():
    final_message = "Your journey is complete!"  # Default final message
    return render_template(
        'game_summary.html', 
        player_money=player_money,  # Use global variables for money
        player_score=player_score,  # Use global variables for score
        final_message=final_message
    )

# End Game Page
@app.route('/end_game', methods=['GET'])
def end_game():
    return render_template('end_game.html')
