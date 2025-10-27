# Casino Roulette MCP Server

A Model Context Protocol (MCP) server that simulates a casino roulette wheel with ASCII art visualization.

## Purpose

This MCP server provides a fun and interactive interface for AI assistants to simulate roulette spins, complete with visual ASCII art representations of the wheel and comprehensive game information.

## Features

### Current Implementation
- **`spin_roulette`** - Spins the roulette wheel and displays the result with ASCII art
- **`get_roulette_info`** - Provides comprehensive roulette rules and betting information
- **`check_number_color`** - Checks the color of any specific roulette number (0-36)
- **`multi_spin`** - Performs multiple spins and provides statistical analysis

## Prerequisites

- Docker Desktop with MCP Toolkit enabled
- Docker MCP CLI plugin (`docker mcp` command)

## Installation

See the step-by-step instructions provided with the files.

## Usage Examples

In Claude Desktop, you can ask:
- "Spin the roulette wheel"
- "Launch the roulette and show me the result"
- "What color is number 17 in roulette?"
- "Spin the roulette 10 times and show me the statistics"
- "Explain the rules of roulette"
- "What are the red numbers in roulette?"
- "Do a multi-spin of 20 rounds"

## Features in Detail

### Spin Roulette
- Generates a random number between 0 and 36
- Determines the correct color (red, black, or green for 0)
- Displays a beautiful ASCII art visualization of the wheel
- Shows the winning number prominently
- Includes additional information (odd/even, high/low)

### Number Color Checker
- Verify the color of any roulette number
- Useful for understanding the game layout
- Shows additional properties (odd/even, range)

### Multi-Spin Statistics
- Perform multiple spins (1-100)
- Track color distribution
- Compare actual vs expected probabilities
- Analyze house edge performance

### Game Information
- Complete list of red and black numbers
- Betting options explained
- Payout odds for different bet types
- General roulette rules

## Architecture

```
Claude Desktop → MCP Gateway → Roulette MCP Server → Random Number Generator
                                       ↓
                                  ASCII Art Engine
```

## Development

### Local Testing

```bash
# Run directly for testing
python roulette_server.py

# Test MCP protocol
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | python roulette_server.py
```

### Adding New Tools

1. Add the function to `roulette_server.py`
2. Decorate with `@mcp.tool()`
3. Update the catalog entry with the new tool name
4. Rebuild the Docker image

## Game Rules Reference

### Number Colors
- **Red (18 numbers)**: 1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36
- **Black (18 numbers)**: 2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35
- **Green (1 number)**: 0

### Bet Types
- **Straight Up**: Single number (35:1)
- **Red/Black**: Color bet (1:1)
- **Odd/Even**: Parity bet (1:1)
- **Low/High**: 1-18 or 19-36 (1:1)
- **Dozens**: 12-number groups (2:1)
- **Columns**: Vertical columns (2:1)

## Troubleshooting

### Tools Not Appearing
- Verify Docker image built successfully
- Check catalog and registry files
- Ensure Claude Desktop config includes custom catalog
- Restart Claude Desktop

### Unexpected Results
- The server uses Python's random module for true randomness
- Each spin is independent of previous spins
- Statistical variations are normal in small sample sizes

## Fun Facts

- The roulette wheel layout isn't random - it's designed to alternate colors and distribute numbers evenly
- The sum of all roulette numbers (1-36) equals 666
- European roulette has better odds than American (single vs double zero)
- The most famous roulette bet won £2 million at the Plaza Hotel in 2004

## Security Considerations

- No external API calls or network access required
- Running as non-root user in Docker
- No sensitive data handling
- Pure simulation with no real money involved

## License

MIT License