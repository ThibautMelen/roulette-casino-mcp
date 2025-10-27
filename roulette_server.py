#!/usr/bin/env python3
"""
Simple Casino Roulette MCP Server - Simulates a roulette wheel with ASCII art
"""
import os
import sys
import logging
import random
from datetime import datetime, timezone
from mcp.server.fastmcp import FastMCP

# Configure logging to stderr
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("roulette-server")

# Initialize MCP server - NO PROMPT PARAMETER!
mcp = FastMCP("roulette")

# Roulette configuration
RED_NUMBERS = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
BLACK_NUMBERS = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}

# === UTILITY FUNCTIONS ===
def get_number_color(number):
    """Determine the color of a roulette number."""
    if number == 0:
        return "green"
    elif number in RED_NUMBERS:
        return "red"
    else:
        return "black"

def create_roulette_ascii(number, color):
    """Create ASCII art representation of the roulette wheel with the winning number."""
    # Color emoji representation
    color_symbol = "🟢" if color == "green" else ("🔴" if color == "red" else "⚫")
    
    # Create the ASCII wheel
    ascii_art = f"""
    ╔════════════════════════════════════════╗
    ║         🎰 CASINO ROULETTE 🎰         ║
    ╠════════════════════════════════════════╣
    ║                                        ║
    ║           ╭──────────────╮            ║
    ║         ╱                  ╲          ║
    ║       ╱    ┌──────────┐      ╲        ║
    ║      │     │          │       │       ║
    ║     │      │    {number:2d}    │        │      ║
    ║     │      │  {color_symbol}  {color_symbol}  │        │      ║
    ║     │      │          │        │      ║
    ║      │     └──────────┘       │       ║
    ║       ╲                      ╱        ║
    ║         ╲__________________╱          ║
    ║                                        ║
    ║            🎲 WINNER! 🎲               ║
    ║                                        ║
    ║        Number: {number:2d}                      ║
    ║        Color:  {color:<8s}                ║
    ║                                        ║
    ╚════════════════════════════════════════╝
    """
    return ascii_art

def create_simple_wheel():
    """Create a simple spinning animation frame."""
    frames = [
        "  ╱─╲\n │ ○ │\n  ╲─╱",
        "  ╱─╲\n │ ● │\n  ╲─╱",
        "  ╱─╲\n │ ◐ │\n  ╲─╱",
        "  ╱─╲\n │ ◑ │\n  ╲─╱"
    ]
    return random.choice(frames)

# === MCP TOOLS ===
@mcp.tool()
async def spin_roulette() -> str:
    """Spin the roulette wheel and get a random number with its color and ASCII visualization."""
    logger.info("Spinning the roulette wheel")
    
    try:
        # Generate random number (0-36)
        winning_number = random.randint(0, 36)
        
        # Determine the color
        color = get_number_color(winning_number)
        
        # Create the ASCII art
        ascii_art = create_roulette_ascii(winning_number, color)
        
        # Log the result
        logger.info(f"Roulette result: {winning_number} ({color})")
        
        # Return the formatted result
        return f"""🎰 ROULETTE SPIN RESULT 🎰
{ascii_art}

📊 RESULT SUMMARY:
━━━━━━━━━━━━━━━━━━━━
• Number: {winning_number}
• Color: {color.upper()}
• Type: {'ZERO' if winning_number == 0 else 'EVEN' if winning_number % 2 == 0 else 'ODD'}
• Range: {'N/A' if winning_number == 0 else 'LOW (1-18)' if winning_number <= 18 else 'HIGH (19-36)'}
━━━━━━━━━━━━━━━━━━━━

✅ Spin complete! The ball has landed on {winning_number} ({color})."""
        
    except Exception as e:
        logger.error(f"Error spinning roulette: {e}")
        return f"❌ Error: Failed to spin the roulette wheel - {str(e)}"

@mcp.tool()
async def get_roulette_info() -> str:
    """Get information about roulette rules and number colors."""
    logger.info("Retrieving roulette information")
    
    try:
        info = """🎰 ROULETTE INFORMATION 🎰
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 GAME RULES:
• Numbers range from 0 to 36
• 0 is GREEN (house advantage)
• 18 numbers are RED
• 18 numbers are BLACK

🔴 RED NUMBERS:
1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36

⚫ BLACK NUMBERS:
2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35

🟢 GREEN NUMBER:
0 (Zero - House Edge)

📊 BETTING OPTIONS:
• Single Number: Bet on any specific number (0-36)
• Red/Black: Bet on the color
• Odd/Even: Bet on odd or even numbers
• Low/High: Low (1-18) or High (19-36)
• Dozens: 1st (1-12), 2nd (13-24), 3rd (25-36)
• Columns: 1st, 2nd, or 3rd column

🎲 ODDS:
• Single Number: 35:1 payout
• Color (Red/Black): 1:1 payout  
• Odd/Even: 1:1 payout
• Low/High: 1:1 payout
• Dozens/Columns: 2:1 payout

━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
        
        return f"✅ {info}"
        
    except Exception as e:
        logger.error(f"Error getting roulette info: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def check_number_color(number: str = "") -> str:
    """Check the color of a specific roulette number."""
    logger.info(f"Checking color for number: {number}")
    
    # Check for empty input
    if not number.strip():
        return "❌ Error: Please provide a number between 0 and 36"
    
    try:
        # Convert to integer
        num = int(number.strip())
        
        # Validate range
        if num < 0 or num > 36:
            return f"❌ Error: Number must be between 0 and 36 (provided: {num})"
        
        # Get the color
        color = get_number_color(num)
        
        # Create a small visual representation
        color_symbol = "🟢" if color == "green" else ("🔴" if color == "red" else "⚫")
        
        result = f"""📊 NUMBER COLOR CHECK
━━━━━━━━━━━━━━━━━━━━━
Number: {num}
Color: {color.upper()} {color_symbol}
Type: {'ZERO' if num == 0 else 'EVEN' if num % 2 == 0 else 'ODD'}
Range: {'N/A' if num == 0 else 'LOW (1-18)' if num <= 18 else 'HIGH (19-36)'}
━━━━━━━━━━━━━━━━━━━━━"""
        
        return f"✅ {result}"
        
    except ValueError:
        return f"❌ Error: Invalid number format: {number}"
    except Exception as e:
        logger.error(f"Error checking number color: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def multi_spin(spins: str = "5") -> str:
    """Spin the roulette wheel multiple times and show statistics."""
    logger.info(f"Performing multiple spins: {spins}")
    
    # Validate input
    if not spins.strip():
        spins = "5"
    
    try:
        # Convert to integer
        num_spins = int(spins.strip())
        
        # Validate range (1-100 spins max)
        if num_spins < 1:
            return "❌ Error: Number of spins must be at least 1"
        if num_spins > 100:
            return "❌ Error: Maximum 100 spins allowed"
        
        # Perform spins
        results = []
        red_count = 0
        black_count = 0
        green_count = 0
        
        for i in range(num_spins):
            number = random.randint(0, 36)
            color = get_number_color(number)
            results.append((number, color))
            
            if color == "red":
                red_count += 1
            elif color == "black":
                black_count += 1
            else:
                green_count += 1
        
        # Format results
        spin_details = "\n".join([
            f"  Spin {i+1:3d}: {num:2d} ({color})" 
            for i, (num, color) in enumerate(results)
        ])
        
        # Calculate statistics
        red_pct = (red_count / num_spins) * 100
        black_pct = (black_count / num_spins) * 100
        green_pct = (green_count / num_spins) * 100
        
        result = f"""🎰 MULTI-SPIN RESULTS 🎰
━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 INDIVIDUAL SPINS:
{spin_details}

📊 STATISTICS ({num_spins} spins):
━━━━━━━━━━━━━━━━━━━━━
🔴 Red:   {red_count:3d} ({red_pct:.1f}%)
⚫ Black: {black_count:3d} ({black_pct:.1f}%)
🟢 Green: {green_count:3d} ({green_pct:.1f}%)
━━━━━━━━━━━━━━━━━━━━━

📈 ANALYSIS:
• Most frequent color: {('Red' if red_count > black_count and red_count > green_count else 'Black' if black_count > green_count else 'Green')}
• House edge hits (0): {green_count}
• Expected green %: 2.7% (actual: {green_pct:.1f}%)"""
        
        return f"✅ {result}"
        
    except ValueError:
        return f"❌ Error: Invalid number format: {spins}"
    except Exception as e:
        logger.error(f"Error in multi-spin: {e}")
        return f"❌ Error: {str(e)}"

# === SERVER STARTUP ===
if __name__ == "__main__":
    logger.info("Starting Casino Roulette MCP server...")
    logger.info("Server ready to spin the wheel!")
    
    try:
        mcp.run(transport='stdio')
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)