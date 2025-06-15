import json
import time
import os
from collections import defaultdict

def print_banner(winner_song, winner_votes):
    banner = f"""
\033[1;33m
╔══════════════════════════════════════════════════════╗
║              🎉 EUROVISION CHAMPION! 🎉             ║
╠══════════════════════════════════════════════════════╣
║         🏆 Overall Winner: Song {winner_song} with {winner_votes} votes        ║
╚══════════════════════════════════════════════════════╝
\033[0m
"""
    print(banner)

# Lokale paths - consistent met shuffle1
input_file = "/output/italy_votes_reduced.json"
output_file = "/results/italy_ranking.txt"
html_output = "/results/eurovision_results.html"

# Wacht op input van shuffle1 (via rclone sync)
while not os.path.exists(input_file):
    print(f"Waiting for {input_file}...")
    time.sleep(2)

try:
    with open(input_file, "r") as f:
        data = json.load(f)
    
    # Aggregeer stemmen per liedje
    total_votes = defaultdict(int)
    for entry in data:
        for vote in entry["votes"]:
            song_number = vote["song_number"]
            count = vote["count"]
            total_votes[song_number] += count
    
    # Sorteer op stemmen
    final_ranking = sorted(total_votes.items(), key=lambda x: -x[1])
    
    # Genereer text output
    lines = []
    lines.append("\n\033[1;36mEurovision Overall Vote Ranking:\033[0m\n")
    
    for i, (song, votes) in enumerate(final_ranking, 1):
        lines.append(f"{i}. Song {song}: {votes} votes")
    
    if final_ranking:
        winner_song, winner_votes = final_ranking[0]
        lines.append(f"\n\033[1;32mOverall Winner: Song {winner_song} with {winner_votes} votes\033[0m")
        print_banner(winner_song, winner_votes)
    
    # Print en sla text bestand op
    print("\n".join(lines))
    
    # Zorg dat results directory bestaat
    os.makedirs("/results", exist_ok=True)
    
    with open(output_file, "w") as f:
        f.write("\n".join(lines))
    
    # Genereer HTML output (zoals in je documentatie)
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Eurovision 2025 Results</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .winner {{ color: gold; font-size: 24px; font-weight: bold; }}
        .ranking {{ margin: 20px 0; }}
    </style>
</head>
<body>
    <h1>🎉 Eurovision 2025 Official Results 🎉</h1>
    <div class="winner">🏆 Winner: Song {winner_song} with {winner_votes} votes</div>
    <div class="ranking">
        <h2>Final Ranking:</h2>
        <ol>
"""
    
    for song, votes in final_ranking:
        html_content += f"            <li>Song {song}: {votes} votes</li>\n"
    
    html_content += """
        </ol>
    </div>
</body>
</html>
"""
    
    with open(html_output, "w") as f:
        f.write(html_content)
    
    print(f"\nResults saved to {output_file}")
    print(f"HTML results saved to {html_output}")

except FileNotFoundError:
    print(f"File '{input_file}' not found.")
except json.JSONDecodeError:
    print(f"Error decoding JSON from '{input_file}'.")
