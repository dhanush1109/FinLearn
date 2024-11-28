from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import logging
import secrets  # Used for generating a more secure secret key

app = Flask(__name__)
# Generate a secure secret key and regenerate on each server restart
app.secret_key = secrets.token_hex(32)

# Set up logging
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s: %(message)s')

def reset_game_session():
    """Completely reset game session variables."""
    logging.debug("Completely resetting game session variables.")
    session.clear()  # Clear ALL existing session data
    session['player_money'] = 1000
    session['player_score'] = 0
    session['challenge_number'] = 1
    session['current_region'] = 1
    session['completed_challenges'] = {}
    logging.debug(f"Game session reset. Initial state: {dict(session)}")

@app.before_request
def before_request():
    """Ensure game session is initialized before each request."""
    logging.debug(f"Before request: Endpoint is {request.endpoint}")
    
    # Skip initialization for static files and None endpoint
    if request.endpoint in ['static', None]:
        return

    # Ensure game session is properly initialized
    if 'player_money' not in session:
        logging.debug("Game session not found. Initializing fresh session.")
        reset_game_session()

@app.route('/')
def start():
    logging.debug("Navigating to the start page.")
    # Ensure fresh start when navigating to home
    reset_game_session()
    return render_template('start.html')

@app.route('/start', methods=['POST'])
def start_game():
    # Get the username from the request body
    data = request.get_json()
    username = data.get('username')
    
    if username:
        # Log the username and reset game session
        logging.debug(f"Username received: {username}")
        reset_game_session()  # Reset game session on new game start
        return jsonify({"message": "Username received successfully!"}), 200
    else:
        return jsonify({"message": "No username received!"}), 400

@app.route('/instructions')
def instructions():
    logging.debug("Navigating to the instructions page.")
    return render_template('instructions.html')

@app.route('/regions')
def regions():
    logging.debug("Navigating to the regions selection page.")
    return render_template('regions.html')

@app.route('/region1', methods=['GET', 'POST'])
def region1():
    logging.debug(f"Navigating to Region 1: Player money = {session.get('player_money', 1000)}, "
                  f"Player score = {session.get('player_score', 0)}")
    # Ensure we're starting from the first challenge in Region 1
    session['current_region'] = 1
    session['challenge_number'] = 1
    session['completed_challenges'] = {}
    return render_template('region1.html', 
                           player_money=session.get('player_money', 1000), 
                           player_score=session.get('player_score', 0))

@app.route('/region1/challenge1', methods=['GET', 'POST'])
def region1_challenge1():
    logging.debug("Accessing Region 1 Challenge 1.")
    
    # Reset this specific challenge tracking to prevent auto-redirect
    if 'completed_challenges' not in session:
        session['completed_challenges'] = {}
    session['completed_challenges']['region1_challenge1'] = False
    
    if request.method == 'POST':
        investment_choice = request.form['investment_choice']
        logging.debug(f"Received POST request. Investment choice: {investment_choice}")

        # Handle Challenge 1: Stock Opportunity
        if investment_choice == 'a':
            session['player_money'] += 37.5  # 15% return on $250
            session['player_score'] += 10  # Points for high-risk, high-return investment
            logging.debug("Chose option A: Updated money and score.")
        elif investment_choice == 'b':
            session['player_money'] += 25  # No gain or loss on $500
            session['player_score'] += 5  # Points for moderate risk, no return
            logging.debug("Chose option B: Updated money and score.")
        elif investment_choice == 'c':
            session['player_money'] += 67.5  # 10% return on $150 (Tech) + 5% on $350 (Bonds)
            session['player_score'] += 15  # Points for diversification (lower risk)
            logging.debug("Chose option C: Updated money and score.")

        # Mark this challenge as completed
        session['completed_challenges']['region1_challenge1'] = True
        
        # Move to Challenge 2
        session['challenge_number'] = 2
        logging.debug(f"Challenge completed. Moving to Challenge 2: Money = {session['player_money']}, "
                      f"Score = {session['player_score']}")
        return redirect(url_for('region1_challenge2'))

    logging.debug(f"Rendering Region 1 Challenge 1: Money = {session.get('player_money', 1000)}, "
                  f"Score = {session.get('player_score', 0)}")
    return render_template('region1_challenge1.html', 
                           player_money=session.get('player_money', 1000), 
                           player_score=session.get('player_score', 0))

@app.route('/region1/challenge2', methods=['GET', 'POST'])
def region1_challenge2():
    logging.debug("Accessing Region 1 Challenge 2.")
    
    # Reset this specific challenge tracking to prevent auto-redirect
    if 'completed_challenges' not in session:
        session['completed_challenges'] = {}
    session['completed_challenges']['region1_challenge2'] = False
    
    if request.method == 'POST':
        investment_choice = request.form['investment_choice']
        logging.debug(f"Received POST request. Investment choice: {investment_choice}")

        # Handle Challenge 2: Gold vs. Real Estate
        if investment_choice == 'a':
            session['player_money'] += 40  # 8% return on $500 for gold
            session['player_score'] += 10  # Points for short-term investment
            logging.debug("Chose option A: Updated money and score.")
        elif investment_choice == 'b':
            session['player_money'] += 75  # 15% return on $500 for real estate after 3 years
            session['player_score'] += 20  # Points for long-term growth investment
            logging.debug("Chose option B: Updated money and score.")
        elif investment_choice == 'c':
            session['player_money'] += 57.5  # Gold +8% on $250, Real Estate +15% on $250
            session['player_score'] += 15  # Points for balanced investment
            logging.debug("Chose option C: Updated money and score.")

        # Mark this challenge as completed
        session['completed_challenges']['region1_challenge2'] = True
        
        # Move to Region 2
        session['current_region'] = 2
        session['challenge_number'] = 1
        logging.debug(f"Challenge completed. Moving to Region 2: Money = {session['player_money']}, "
                      f"Score = {session['player_score']}")
        return redirect(url_for('region2'))

    logging.debug(f"Rendering Region 1 Challenge 2: Money = {session.get('player_money', 1000)}, "
                  f"Score = {session.get('player_score', 0)}")
    return render_template('region1_challenge2.html', 
                           player_money=session.get('player_money', 1000), 
                           player_score=session.get('player_score', 0))

@app.route('/region2', methods=['GET', 'POST'])
def region2():
    logging.debug(f"Navigating to Region 2: Player money = {session.get('player_money', 1000)}, "
                  f"Player score = {session.get('player_score', 0)}")
    # Set region and challenge tracking
    session['current_region'] = 2
    session['challenge_number'] = 1
    session['completed_challenges'] = {}
    return render_template('region2.html', 
                           player_money=session.get('player_money', 1000), 
                           player_score=session.get('player_score', 0))

@app.route('/region2/challenge1', methods=['GET', 'POST'])
def region2_challenge1():
    logging.debug("=== Starting Region 2 Challenge 1 ===")
    logging.debug(f"Request Method: {request.method}")
    logging.debug(f"Session before processing: {session}")
    logging.debug(f"Form data: {request.form}")
    
    if 'completed_challenges' not in session:
        logging.debug("Initializing completed_challenges in session")
        session['completed_challenges'] = {}
    session['completed_challenges']['region2_challenge1'] = False
    
    if request.method == 'POST':
        try:
            expense_choice = request.form['expense_choice']
            logging.debug(f"Expense choice received: {expense_choice}")
        except KeyError:
            logging.error("Missing expense_choice in form data")
            return "Expense choice required", 400
            
        try:
            if expense_choice == 'a':
                logging.debug("Processing choice A: Using portfolio")
                session['player_money'] -= 200
                session['player_score'] += 5
            elif expense_choice == 'b':
                logging.debug("Processing choice B: Using savings")
                session['player_score'] += 15
            elif expense_choice == 'c':
                logging.debug("Processing choice C: Borrowing")
                session['player_money'] -= 220  # $200 + $20 interest
                session['player_score'] += 10
            else:
                logging.error(f"Invalid expense choice: {expense_choice}")
                return "Invalid expense choice", 400
                
            session['completed_challenges']['region2_challenge1'] = True
            session['challenge_number'] = 2
            return redirect(url_for('region2_challenge2'))
            
        except Exception as e:
            logging.error(f"Error processing expense choice: {str(e)}")
            return "Error processing expense", 500

    return render_template('region2_challenge1.html', 
                         player_money=session.get('player_money', 1000), 
                         player_score=session.get('player_score', 0))

@app.route('/region2/challenge2', methods=['GET', 'POST'])
def region2_challenge2():
    logging.debug("=== Starting Region 2 Challenge 2: Luxury Temptation ===")
    logging.debug(f"Request Method: {request.method}")
    logging.debug(f"Session before processing: {session}")
    logging.debug(f"Form data: {request.form}")
    
    if 'completed_challenges' not in session:
        logging.debug("Initializing completed_challenges in session")
        session['completed_challenges'] = {}
    session['completed_challenges']['region2_challenge2'] = False
    
    if request.method == 'POST':
        try:
            expense_choice = request.form['expense_choice']
            logging.debug(f"Luxury expense choice received: {expense_choice}")
        except KeyError:
            logging.error("Missing expense_choice in form data")
            return "Expense choice required", 400
            
        try:
            current_money = session.get('player_money', 1000)
            current_score = session.get('player_score', 0)
            
            if expense_choice == 'a':
                logging.debug("Processing choice A: Immediate luxury purchase")
                session['player_money'] = current_money - 200  # Immediate loss for luxury purchase
                session['player_score'] = current_score - 5   # Points for impulsive spending
            elif expense_choice == 'b':
                logging.debug("Processing choice B: Avoiding purchase")
                session['player_money'] = current_money      # No change in portfolio
                session['player_score'] = current_score + 10  # Points for avoiding impulsive buying
            elif expense_choice == 'c':
                logging.debug("Processing choice C: Strategic purchase and resale")
                session['player_money'] = current_money + 220  # Gain from resale after 3 turns
                session['player_score'] = current_score + 20   # Points for making a wise purchase
            else:
                logging.error(f"Invalid luxury expense choice: {expense_choice}")
                return "Invalid choice", 400
                
            session['completed_challenges']['region2_challenge2'] = True
            session['current_region'] = 3
            session['challenge_number'] = 1
            
            logging.debug(f"Challenge completed. Moving to Region 3: Money = {session['player_money']}, "
                         f"Score = {session['player_score']}")
            return redirect(url_for('region3'))
            
        except Exception as e:
            logging.error(f"Error processing luxury choice: {str(e)}")
            return "Error processing choice", 500

    current_money = session.get('player_money', 1000)
    current_score = session.get('player_score', 0)
    
    logging.debug(f"Rendering Region 2 Challenge 2: Money = {current_money}, Score = {current_score}")
    return render_template('region2_challenge2.html', 
                         player_money=current_money,
                         player_score=current_score)

@app.route('/region3', methods=['GET', 'POST'])
def region3():
    logging.debug(f"Navigating to Region 3: Player money = {session.get('player_money', 1000)}, "
                  f"Player score = {session.get('player_score', 0)}")
    # Set region and challenge tracking
    session['current_region'] = 3
    session['challenge_number'] = 1
    session['completed_challenges'] = {}
    return render_template('region3.html', 
                           player_money=session.get('player_money', 1000), 
                           player_score=session.get('player_score', 0))

@app.route('/region3/challenge1', methods=['GET', 'POST'])
def region3_challenge1():
    logging.debug("Accessing Region 3 Challenge 1.")
    
    # Initialize session variables if not exist
    if 'completed_challenges' not in session:
        session['completed_challenges'] = {}
    if 'player_money' not in session:
        session['player_money'] = 1000
    if 'player_score' not in session:
        session['player_score'] = 0
    
    session['completed_challenges']['region3_challenge1'] = False
    
    if request.method == 'POST':
        # Ensure the form field matches the HTML
        reinvest_choice = request.form.get('reinvest_choice')
        logging.debug(f"Received POST request. Reinvestment choice: {reinvest_choice}")
        
        # Handle different choices
        if reinvest_choice == 'a':
            session['player_money'] -= 50  # Spend immediately
            session['player_score'] += 5
        elif reinvest_choice == 'b':
            session['player_money'] += 60  # Reinvest
            session['player_score'] += 15
        elif reinvest_choice == 'c':
            session['player_money'] += 30  # Savings account
            session['player_score'] += 10
        else:
            # Handle case where no choice is selected
            flash('Please select an option')
            return render_template('region3_challenge1.html', 
                                   player_money=session['player_money'], 
                                   player_score=session['player_score'])
        
        session['completed_challenges']['region3_challenge1'] = True
        session['challenge_number'] = 2
        logging.debug(f"Challenge completed. Moving to Challenge 2: Money = {session['player_money']}, Score = {session['player_score']}")
        
        return redirect(url_for('region3_challenge2'))
    
    return render_template('region3_challenge1.html', 
                           player_money=session['player_money'], 
                           player_score=session['player_score'])

@app.route('/region3/challenge2', methods=['GET', 'POST'])
def region3_challenge2():
    logging.debug("Accessing Region 3 Challenge 2.")
    
    # Ensure we have the data from Challenge 1
    if 'player_money' not in session:
        session['player_money'] = 1000
    if 'player_score' not in session:
        session['player_score'] = 0
    
    if 'completed_challenges' not in session:
        session['completed_challenges'] = {}
    
    # Ensure Challenge 1 was completed before accessing Challenge 2
    if not session.get('completed_challenges', {}).get('region3_challenge1', False):
        flash('You must complete Challenge 1 first!')
        return redirect(url_for('region3_challenge1'))
    
    session['completed_challenges']['region3_challenge2'] = False
    
    if request.method == 'POST':
        # Get the investment choice from the form
        gains_choice = request.form.get('gains_choice')
        logging.debug(f"Received POST request. Gains choice: {gains_choice}")

        # Handle Challenge 2: Investment Choices
        if gains_choice == 'a':
            # 10% gain in 6 months
            session['player_money'] += 50
            session['player_score'] += 10
        elif gains_choice == 'b':
            # 20% gain in 2 years
            session['player_money'] += 100
            session['player_score'] += 20
        elif gains_choice == 'c':
            # Half now, half later
            session['player_money'] += 150
            session['player_score'] += 15
        else:
            # Handle case where no choice is selected
            flash('Please select an option')
            return render_template('region3_challenge2.html', 
                                   player_money=session['player_money'], 
                                   player_score=session['player_score'])
        
        session['completed_challenges']['region3_challenge2'] = True
        session['current_region'] = 4
        session['challenge_number'] = 1
        logging.debug(f"Challenge completed. Moving to Region 4: Money = {session['player_money']}, "
                      f"Score = {session['player_score']}")
        
        return redirect(url_for('region4'))

    return render_template('region3_challenge2.html', 
                           player_money=session['player_money'], 
                           player_score=session['player_score'])

@app.route('/region4', methods=['GET', 'POST'])
def region4():
    logging.debug(f"Entering Region 4. Initial Player State: "
                  f"Money = {session.get('player_money', 1000)}, "
                  f"Score = {session.get('player_score', 0)}")
    
    session['current_region'] = 4
    session['challenge_number'] = 1
    session['completed_challenges'] = {}
    
    logging.debug("Region 4 setup complete. Ready to render template.")
    return render_template('region4.html', 
                           player_money=session.get('player_money', 1000), 
                           player_score=session.get('player_score', 0))

@app.route('/region4/challenge1', methods=['GET', 'POST'])
def region4_challenge1():
    logging.debug("Entering Region 4 Challenge 1.")
    
    if 'completed_challenges' not in session:
        session['completed_challenges'] = {}
    session['completed_challenges']['region4_challenge1'] = False
    
    logging.debug("Session data initialized for Challenge 1.")
    
    if request.method == 'POST':
        # Corrected form field reference
        investment_choice = request.form['market_choice']
        logging.debug(f"Challenge 1 POST request received. Investment choice: {investment_choice}")
        
        if investment_choice == 'a':
            session['player_money'] += 50  # Timing market entry during growth phase
            session['player_score'] += 15  # Good economic foresight
            logging.debug("Choice A: Growth phase timing. Money +45, Score +15.")
        elif investment_choice == 'b':
            session['player_money'] += 200  # Safe investments during downturn
            session['player_score'] += 10  # Conservative choice
            logging.debug("Choice B: Safe investments. Money +25, Score +10.")
        elif investment_choice == 'c':
            session['player_money'] += 100  # Mixed strategy
            session['player_score'] += 12  # Moderate success
            logging.debug("Choice C: Mixed strategy. Money +35, Score +12.")
        else:
            logging.warning(f"Unexpected investment choice: {investment_choice}")

        session['completed_challenges']['region4_challenge1'] = True
        session['challenge_number'] = 2
        logging.debug(f"Challenge 1 completed. Updated Player State: "
                      f"Money = {session['player_money']}, Score = {session['player_score']}")
        
        return redirect(url_for('region4_challenge2'))

    logging.debug("Rendering Region 4 Challenge 1 template.")
    return render_template('region4_challenge1.html', 
                           player_money=session.get('player_money', 1000), 
                           player_score=session.get('player_score', 0))

@app.route('/region4/challenge2', methods=['GET', 'POST'])
def region4_challenge2():
    logging.debug("Entering Region 4 Challenge 2.")
    
    # Initialize completed_challenges in session if not already set
    if 'completed_challenges' not in session:
        session['completed_challenges'] = {}
    session['completed_challenges']['region4_challenge2'] = False
    
    # Retrieve player state from session
    player_money = session.get('player_money', 1000)
    player_score = session.get('player_score', 0)
    logging.debug(f"Player state before Challenge 2: Money = {player_money}, Score = {player_score}")

    if request.method == 'POST':
        # Fetch the choice from the form
        recession_choice = request.form.get('recession_choice')
        logging.debug(f"Challenge 2 POST request received. Recession choice: {recession_choice}")

        if not recession_choice:
            logging.error("No choice selected. Redirecting back to the challenge page.")
            return redirect(url_for('region4_challenge2'))

        # Update session based on player choice
        if recession_choice == 'a':
            player_money += 50  # Safer assets reduce returns
            player_score += 10  # Wise decision to avoid risk
            logging.debug("Choice A: Moved to safer assets. Money -10, Score +10.")
        elif recession_choice == 'b':
            player_money = player_money   # No immediate action
            player_score -= 5   # Risk of loss during recession
            logging.debug("Choice B: Kept portfolio as is. Money +20, Score -5.")
        elif recession_choice == 'c':
            player_money += 250   # Held cash
            player_score += 15  # Avoided market risk
            logging.debug("Choice C: Withdrew to cash. Money +5, Score +15.")
        else:
            logging.warning(f"Unexpected recession choice: {recession_choice}")
            return redirect(url_for('region4_challenge2'))

        # Update session values with new player state
        session['player_money'] = player_money
        session['player_score'] = player_score
        session['completed_challenges']['region4_challenge2'] = True

        # Transition to the next region
        session['current_region'] = 5
        session['challenge_number'] = 1
        logging.debug(f"Challenge 2 completed. Transitioning to Region 5. "
                      f"Updated Player State: Money = {player_money}, "
                      f"Score = {player_score}")
        
        return redirect(url_for('region5'))

    # Render the template with current player state
    logging.debug("Rendering Region 4 Challenge 2 template.")
    return render_template('region4_challenge2.html', 
                           player_money=player_money, 
                           player_score=player_score)


@app.route('/region5', methods=['GET', 'POST'])
def region5():
    logging.debug(f"Navigating to Region 5: Player money = {session.get('player_money', 1000)}, "
                  f"Player score = {session.get('player_score', 0)}")
    session['current_region'] = 5
    session['challenge_number'] = 1
    session['completed_challenges'] = {}
    return render_template('region5.html', 
                           player_money=session.get('player_money', 1000), 
                           player_score=session.get('player_score', 0))

@app.route('/region5/challenge1', methods=['GET', 'POST'])
def region5_challenge1():
    logging.debug("Accessing Region 5 Challenge 1.")

    # Initialize session variables
    if 'completed_challenges' not in session:
        session['completed_challenges'] = {}
    session['completed_challenges']['region5_challenge1'] = False

    # Retrieve player state
    player_money = session.get('player_money', 1000)
    player_score = session.get('player_score', 0)
    retirement_fund = session.get('retirement_fund', 0)

    logging.debug(f"Player state: Money = {player_money}, Score = {player_score}, Retirement Fund = {retirement_fund}")

    if request.method == 'POST':
        # Handle form submission
        retirement_choice = request.form.get('retirement_choice')
        logging.debug(f"Received POST request. Retirement choice: {retirement_choice}")

        if not retirement_choice:
            logging.error("No retirement choice selected.")
            return redirect(url_for('region5_challenge1'))

        # Process choices
        if retirement_choice == 'a':  # Contribute 5% ($50)
            player_money -= 50
            retirement_fund += 50
            player_score += 10  # Steady growth
            logging.debug("Choice A: Contributed 5% to retirement fund.")
        elif retirement_choice == 'b':  # Delay contributions
            player_score -= 15  # Missed opportunity
            logging.debug("Choice B: Delayed retirement contributions.")
        elif retirement_choice == 'c':  # Contribute $500
            player_money -= 500
            retirement_fund += 500
            player_score += 30  # Compounding benefits
            logging.debug("Choice C: Contributed $500 to retirement fund.")
        else:
            logging.warning(f"Unexpected retirement choice: {retirement_choice}")
            return redirect(url_for('region5_challenge1'))

        # Update session variables
        session['player_money'] = player_money
        session['player_score'] = player_score
        session['retirement_fund'] = retirement_fund
        session['completed_challenges']['region5_challenge1'] = True

        logging.debug(f"Updated Player State: Money = {player_money}, Score = {player_score}, Retirement Fund = {retirement_fund}")
        
        # Redirect to Challenge 2
        session['challenge_number'] = 2
        return redirect(url_for('region5_challenge2'))

    # Render template
    return render_template('region5_challenge1.html', 
                           player_money=player_money, 
                           player_score=player_score, 
                           retirement_fund=retirement_fund)

@app.route('/region5/challenge2', methods=['GET', 'POST'])
def region5_challenge2():
    logging.debug("Accessing Region 5 Challenge 2.")

    # Ensure session variables are initialized
    if 'completed_challenges' not in session:
        session['completed_challenges'] = {}
    if 'retirement_fund' not in session:
        session['retirement_fund'] = 100  # Initialize if not set
    if not session['completed_challenges'].get('region5_challenge1'):
        # Double the retirement fund if moving from Challenge 1
        session['retirement_fund'] *= 2

    session['completed_challenges']['region5_challenge2'] = False

    if request.method == 'POST':
        insurance_choice = request.form['insurance_choice']
        logging.debug(f"Received POST request. Insurance choice: {insurance_choice}")

        # Handle the challenge outcomes
        if insurance_choice == 'a':
            session['player_money'] += 100  # Balanced allocation
            session['player_score'] += 15  # Great financial planning
        elif insurance_choice == 'b':
            session['player_money'] += 50  # Aggressive allocation
            session['player_score'] += 10  # Riskier strategy
        elif insurance_choice == 'c':
            session['player_money'] += 40  # Conservative allocation
            session['player_score'] += 5   # Minimal growth

        # Update retirement fund based on choice (optional)
        if insurance_choice == 'a':
            session['retirement_fund'] += 50
        elif insurance_choice == 'c':
            session['retirement_fund'] += 100

        session['completed_challenges']['region5_challenge2'] = True
        logging.debug(f"Challenge completed. Money = {session['player_money']}, "
                      f"Score = {session['player_score']}, Retirement Fund = {session['retirement_fund']}")
        return redirect(url_for('golden_portfolio_test'))

    return render_template('region5_challenge2.html',
                           player_money=session.get('player_money', 1000),
                           player_score=session.get('player_score', 0),
                           retirement_fund=session.get('retirement_fund', 100))


@app.route('/golden_portfolio_test', methods=['GET', 'POST'])
def golden_portfolio_test():
    feedback = None  # Initialize feedback for the user

    # Ensure session variables are initialized
    if 'retirement_fund' not in session:
        session['retirement_fund'] = 0  # Initialize if not set

    # Double the retirement fund as the player enters the test
    session['retirement_fund'] *= 2
    logging.debug(f"Golden Portfolio Test: Retirement Fund doubled to {session['retirement_fund']}.")

    if request.method == 'POST':
        # Retrieve the player's final answer
        final_answer = request.form['final_answer']
        logging.debug(f"Golden Portfolio Test answer received: {final_answer}")

        # Validate the answer
        if final_answer == 'b':
            session['player_money'] += 50  # Best answer
            session['player_score'] += 30  # Significant reward for correct understanding
            logging.debug(f"Correct answer! Money = {session['player_money']}, "
                          f"Score = {session['player_score']}, Retirement Fund = {session['retirement_fund']}")
            return redirect(url_for('game_summary'))
        else:
            feedback = (
                "Incorrect. Compound interest grows wealth exponentially over time. "
                "Try again!"
            )
            logging.debug("Incorrect answer provided.")

    # Render the test page with feedback if the answer is incorrect
    return render_template(
        'golden_portfolio_test.html',
        player_money=session.get('player_money', 1000),
        player_score=session.get('player_score', 0),
        retirement_fund=session.get('retirement_fund', 100),
        feedback=feedback
    )

@app.route('/game_summary', methods=['GET'])
def game_summary():
    # Get values from session or set defaults
    player_money = session.get('player_money', 1000)
    player_score = session.get('player_score', 0)
    retirement_fund = session.get('retirement_fund', 0)
    
    final_message = "Your journey is complete!"
    
    # Render the game summary page with the updated values
    return render_template(
        'game_summary.html', 
        player_money=player_money,
        player_score=player_score,
        retirement_fund=retirement_fund,
        final_message=final_message
    )


@app.route('/end_game', methods=['GET'])
def end_game():
    # Clear session data
    session.clear()
    return render_template('end_game.html')

if __name__ == '__main__':
    app.run(debug=True)
