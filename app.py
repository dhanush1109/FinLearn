import streamlit as st
import random

class GoldenPortfolioGame:
    def __init__(self):
        # Initialize session state keys if not exists
        if 'game_started' not in st.session_state:
            st.session_state.game_started = False
        if 'game_state' not in st.session_state:
            self._reset_game_state()

    def _reset_game_state(self):
        """Reset the game state to initial conditions"""
        st.session_state.game_state = {
            'total_score': 0,
            'current_region_index': 0,
            'current_challenge_index': 0,
            'completed_challenges': [],
            'current_funds': 1000,
            'wisdom_tokens': 0
        }

    def _get_regions(self):
        """Define game regions and challenges"""
        return [
            {
                'name': 'Valley of Ventures (Investing Basics)',
                'challenges': [
                    {
                        'scenario': 'You receive a tip about a promising tech startup.',
                        'choices': [
                            {
                                'text': 'Invest 25% of funds ($250) hoping for high returns',
                                'score': 7.5,
                                'fund_impact': 37.50,
                                'wisdom': 2,
                                'explanation': 'Moderate investment with potential tech returns (+15%)'
                            },
                            {
                                'text': 'Invest 50% of funds ($500) for a higher risk-reward balance',
                                'score': 5.0,
                                'fund_impact': 0,
                                'wisdom': 1,
                                'explanation': 'High risk with uncertain returns (0% return)'
                            },
                            {
                                'text': 'Diversify: Invest in tech company and bonds',
                                'score': 9.0,
                                'fund_impact': 67.50,
                                'wisdom': 3,
                                'explanation': 'Smart diversification (Tech +10%, Bonds +5%)'
                            }
                        ]
                    },
                    {
                        'scenario': 'You can choose between buying gold or real estate.',
                        'choices': [
                            {
                                'text': 'Buy gold, anticipating a short-term price spike',
                                'score': 6.5,
                                'fund_impact': 40,
                                'wisdom': 2,
                                'explanation': 'Quick return (+8%) but limited long-term potential'
                            },
                            {
                                'text': 'Invest in real estate, anticipating long-term growth',
                                'score': 9.0,
                                'fund_impact': 75,
                                'wisdom': 3,
                                'explanation': 'Patient investment with +15% return after 3 years'
                            },
                            {
                                'text': 'Split investment between gold and real estate',
                                'score': 8.0,
                                'fund_impact': 57.50,
                                'wisdom': 2,
                                'explanation': 'Balanced approach with moderate risk'
                            }
                        ]
                    }
                ]
            },
            {
                'name': 'Forest of Finance (Managing Expenses and Saving)',
                'challenges': [
                    {
                        'scenario': 'You need $200 for an urgent repair.',
                        'choices': [
                            {
                                'text': 'Dip into your investments',
                                'score': 5.5,
                                'fund_impact': -200,
                                'wisdom': 1,
                                'explanation': 'Disrupts investment strategy, delays returns'
                            },
                            {
                                'text': 'Use your savings',
                                'score': 9.0,
                                'fund_impact': -200,
                                'wisdom': 3,
                                'explanation': 'Maintains investment integrity, keeps portfolio intact'
                            },
                            {
                                'text': 'Borrow money',
                                'score': 4.0,
                                'fund_impact': -220,
                                'wisdom': 1,
                                'explanation': 'Incurs 10% interest, increases financial burden'
                            }
                        ]
                    },
                    {
                        'scenario': 'You see an expensive relic you want to buy.',
                        'choices': [
                            {
                                'text': 'Buy the relic',
                                'score': 4.0,
                                'fund_impact': -200,
                                'wisdom': 1,
                                'explanation': 'Impulsive purchase reduces portfolio value'
                            },
                            {
                                'text': 'Skip the purchase',
                                'score': 9.0,
                                'fund_impact': 0,
                                'wisdom': 3,
                                'explanation': 'Preserves wealth for better opportunities'
                            },
                            {
                                'text': 'Purchase only if resellable for profit',
                                'score': 7.0,
                                'fund_impact': 20,
                                'wisdom': 2,
                                'explanation': 'Potential for 10% resale value after 3 turns'
                            }
                        ]
                    }
                ]
            },
            {
                'name': 'Canyon of Compounders (Power of Compounding)',
                'challenges': [
                    {
                        'scenario': 'You earned $50 interest from an investment.',
                        'choices': [
                            {
                                'text': 'Spend the money immediately',
                                'score': 4.0,
                                'fund_impact': -50,
                                'wisdom': 1,
                                'explanation': 'Reduces potential for compound growth'
                            },
                            {
                                'text': 'Reinvest the money',
                                'score': 9.0,
                                'fund_impact': 10,
                                'wisdom': 3,
                                'explanation': 'Compound growth increases portfolio by 20%'
                            },
                            {
                                'text': 'Put it in a savings account',
                                'score': 6.0,
                                'fund_impact': 1,
                                'wisdom': 2,
                                'explanation': 'Low interest rate limits growth potential'
                            }
                        ]
                    },
                    {
                        'scenario': 'Choose between short-term and long-term returns.',
                        'choices': [
                            {
                                'text': 'Take a 10% gain in 6 months',
                                'score': 6.0,
                                'fund_impact': 50,
                                'wisdom': 2,
                                'explanation': 'Quick return but limited long-term potential'
                            },
                            {
                                'text': 'Wait for a 20% gain in 2 years',
                                'score': 9.0,
                                'fund_impact': 100,
                                'wisdom': 3,
                                'explanation': 'Patient approach yields higher returns'
                            },
                            {
                                'text': 'Take half now and half later',
                                'score': 7.0,
                                'fund_impact': 50,
                                'wisdom': 2,
                                'explanation': 'Balanced approach with moderate returns'
                            }
                        ]
                    }
                ]
            },
            {
                'name': 'City of Cycles (Understanding Economic Cycles)',
                'challenges': [
                    {
                        'scenario': 'The market has recently declined.',
                        'choices': [
                            {
                                'text': 'Invest heavily, hoping for recovery',
                                'score': 4.0,
                                'fund_impact': -450,
                                'wisdom': 1,
                                'explanation': 'High risk, significant potential loss'
                            },
                            {
                                'text': 'Wait to see if the market falls further',
                                'score': 5.0,
                                'fund_impact': 0,
                                'wisdom': 2,
                                'explanation': 'Missed opportunity for growth'
                            },
                            {
                                'text': 'Invest gradually over time',
                                'score': 9.0,
                                'fund_impact': -50,
                                'wisdom': 3,
                                'explanation': 'Dollar-cost averaging minimizes risk'
                            }
                        ]
                    },
                    {
                        'scenario': 'A recession is forecast.',
                        'choices': [
                            {
                                'text': 'Move investments to safer assets',
                                'score': 9.0,
                                'fund_impact': -30,
                                'wisdom': 3,
                                'explanation': 'Protects portfolio during downturn'
                            },
                            {
                                'text': 'Keep portfolio as is',
                                'score': 4.0,
                                'fund_impact': -200,
                                'wisdom': 1,
                                'explanation': 'Exposes portfolio to significant market risk'
                            },
                            {
                                'text': 'Withdraw funds to hold cash',
                                'score': 6.0,
                                'fund_impact': 0,
                                'wisdom': 2,
                                'explanation': 'Misses potential recovery opportunity'
                            }
                        ]
                    }
                ]
            },
            {
                'name': 'Summit of Strategy (Financial Planning)',
                'challenges': [
                    {
                        'scenario': 'You are offered an option to start a retirement fund.',
                        'choices': [
                            {
                                'text': 'Contribute 5% now and increase over time',
                                'score': 8.0,
                                'fund_impact': 52.50,
                                'wisdom': 2,
                                'explanation': 'Balanced approach to long-term savings'
                            },
                            {
                                'text': 'Delay retirement planning',
                                'score': 4.0,
                                'fund_impact': 0,
                                'wisdom': 1,
                                'explanation': 'Misses compounding growth opportunities'
                            },
                            {
                                'text': 'Put a large amount now for compounding',
                                'score': 9.0,
                                'fund_impact': 550,
                                'wisdom': 3,
                                'explanation': 'Maximizes long-term wealth potential'
                            }
                        ]
                    },
                    {
                        'scenario': 'You\'re offered a life insurance plan.',
                        'choices': [
                            {
                                'text': 'Buy it as a safety measure',
                                'score': 8.0,
                                'fund_impact': -100,
                                'wisdom': 3,
                                'explanation': 'Protects against unexpected financial strain'
                            },
                            {
                                'text': 'Skip it to keep funds available',
                                'score': 4.0,
                                'fund_impact': 0,
                                'wisdom': 1,
                                'explanation': 'Exposes to potential future financial risks'
                            },
                            {
                                'text': 'Buy a plan with investment options',
                                'score': 9.0,
                                'fund_impact': 50,
                                'wisdom': 3,
                                'explanation': 'Combines protection with investment growth'
                            }
                        ]
                    }
                ]
            }
        ]

    def render_start_page(self):
        """Render the game start page"""
        st.title("🏆 The Quest for the Golden Portfolio")
        st.write("Embark on a financial adventure to build your wealth!")
        
        st.markdown("""
        ### Game Rules
        - Start with $1,000 initial funds
        - Navigate through 5 regions of financial challenges
        - Make strategic decisions to grow your portfolio
        - Earn wisdom tokens by making smart choices
        - Your final score depends on financial acumen and portfolio growth
        """)
        
        if st.button("Start Your Financial Journey"):
            st.session_state.game_started = True
            self._reset_game_state()
            st.experimental_rerun()

    def render_challenge_page(self):
        """Render the current challenge page"""
        # Get current region and challenge
        regions = self._get_regions()
        current_region_index = st.session_state.game_state['current_region_index']
        current_challenge_index = st.session_state.game_state['current_challenge_index']
        
        region = regions[current_region_index]
        challenge = region['challenges'][current_challenge_index]
        
        # Display header and game state
        st.title(f"{region['name']}")
        st.subheader("Challenge")
        st.write(challenge['scenario'])
        
        # Display current game metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Current Funds", f"${st.session_state.game_state['current_funds']:,.2f}")
        with col2:
            st.metric("Wisdom Tokens", st.session_state.game_state['wisdom_tokens'])
        with col3:
            st.metric("Total Score", f"{st.session_state.game_state['total_score']:.2f}")
        
        # Choice buttons
        for choice in challenge['choices']:
            if st.button(choice['text'], key=f"choice_{choice['text']}"):
                # Update game state
                st.session_state.game_state['current_funds'] += choice['fund_impact']
                st.session_state.game_state['total_score'] += choice['score']
                st.session_state.game_state['wisdom_tokens'] += choice['wisdom']
                
                # Display choice explanation
                st.info(f"Result: {choice['explanation']}")
                
                # Log completed challenge
                st.session_state.game_state['completed_challenges'].append({
                    'region': region['name'],
                    'scenario': challenge['scenario'],
                    'choice': choice['text'],
                    'score': choice['score']
                })
                
                # Move to next challenge or region
                if current_challenge_index + 1 < len(region['challenges']):
                    st.session_state.game_state['current_challenge_index'] += 1
                elif current_region_index + 1 < len(regions):
                    st.session_state.game_state['current_region_index'] += 1
                    st.session_state.game_state['current_challenge_index'] = 0
                else:
                    # Game completed
                    st.session_state.game_state['game_completed'] = True
                
                st.experimental_rerun()

    def render_summary_page(self):
        """Render the game summary page"""
        st.title("🏆 Financial Journey Complete!")
        
        # Calculate summary metrics
        total_score = st.session_state.game_state['total_score']
        final_funds = st.session_state.game_state['current_funds']
        wisdom_tokens = st.session_state.game_state['wisdom_tokens']
        
        # Determine investment rating
        if total_score < 30:
            rating = "Novice Investor"
            advice = "Focus on learning and conservative strategies"
        elif total_score < 50:
            rating = "Developing Investor"
            advice = "You're making progress. Continue learning and diversifying"
        elif total_score < 70:
            rating = "Strategic Investor"
            advice = "Solid financial decisions. Keep refining your approach"
        else:
            rating = "Master Investor"
            advice = "Exceptional financial wisdom and strategic thinking"
        
        # Display summary
        st.metric("Final Portfolio Value", f"${final_funds:,.2f}")
        st.metric("Total Score", f"{total_score:.2f}")
        st.metric("Wisdom Tokens Earned", wisdom_tokens)
        
        st.subheader(f"Investment Rating: {rating}")
        st.write(advice)
        
        # Final test question
        st.subheader("Final Financial Wisdom Test")
        final_question = st.radio(
            "What is the effect of compound interest?",
            [
                "It increases your wealth at a constant rate",
                "It allows your investment to grow exponentially over time",
                "It limits your potential growth"
            ]
        )
        
        # Correct answer check
        if final_question == "It allows your investment to grow exponentially over time":
            st.success("Correct! You truly understand the power of compound interest.")
            st.session_state.game_state['total_score'] += 10
            st.session_state.game_state['wisdom_tokens'] += 5
        else:
            st.warning("Incorrect. Compound interest helps your investments grow exponentially over time.")
        
        # Completed challenges review
        st.subheader("Your Financial Journey")
        for challenge in st.session_state.game_state['completed_challenges']:
            st.write(f"**Region:** {challenge['region']}")
            st.write(f"**Scenario:** {challenge['scenario']}")
            st.write(f"**Choice:** {challenge['choice']}")
            st.write(f"**Score:** {challenge['score']:.2f}")
            st.divider()
        
        # Restart option
        if st.button("Start New Journey"):
            self._reset_game_state()
            st.session_state.game_started = False
            st.experimental_rerun()

def main():
    # Set page configuration
    st.set_page_config(
        page_title="Golden Portfolio Game",
        page_icon="💰",
        layout="wide"
    )
    
    # # Custom CSS for better styling
    # st.markdown("""
    # <style>
    # .stApp {
    #     background-color: #f0f2f6;
    # }
    # .stButton>button {
    #     color: white;
    #     background-color: #4CAF50;
    #     border: none;
    #     padding: 10px 24px;
    #     text-align: center;
    #     text-decoration: none;
    #     display: inline-block;
    #     font-size: 16px;
    #     margin: 4px 2px;
    #     transition-duration: 0.4s;
    #     cursor: pointer;
    # }
    # .stButton>button:hover {
    #     background-color: #45a049;
    # }
    # .stMetric {
    #     background-color: white;
    #     padding: 10px;
    #     border-radius: 5px;
    #     box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    # }
    # </style>
    # """, unsafe_allow_html=True)
    
    game = GoldenPortfolioGame()
    
    # Game flow control
    if not st.session_state.get('game_started', False):
        game.render_start_page()
    elif st.session_state.game_state.get('game_completed', False):
        game.render_summary_page()
    else:
        game.render_challenge_page()

if __name__ == "__main__":
    main()
