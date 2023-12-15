import json

def generate_badge_data(coverage_file):
    with open(coverage_file) as f:
        data = json.load(f)

    total_statements = sum(file_data['summary']['num_statements'] for file_data in data['files'].values())
    covered_statements = sum(file_data['summary']['covered_lines'] for file_data in data['files'].values())
    coverage_percentage = (covered_statements / total_statements) * 100 if total_statements > 0 else 100

    coverage_colors = {
        range(95, 101): 'brightgreen',
        range(90, 95): 'green',
        range(85, 90): 'yellowgreen',
        range(80, 85): 'yellow',
        range(70, 80): 'gold',
        range(60, 70): 'orange',
        range(50, 60): 'darkorange',
        range(40, 50): 'orangered',
        range(30, 40): 'red',
        range(20, 30): 'darkred',
        range(0, 20): 'maroon',
    }

    color = next(
        color for range_, color in coverage_colors.items() if round(coverage_percentage) in range_
    )

    badge_data = {
        "schemaVersion": 1,
        "label": "coverage",
        "message": f"{round(coverage_percentage)}%",
        "color": color
    }

    return json.dumps(badge_data, indent=4)

if __name__=="__main__":
    #coverage json --pretty-print -o coverage.json 
    #write data to badge.json
    badge_data = generate_badge_data('coverage.json')
    with open('badge.json', 'w') as f:
        f.write(badge_data)