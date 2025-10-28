# studious-waffle
pip install -r requirements.txt

⚙️ 1. Project Setup (0.5–1 hour)
🎯 Goal:
Prepare the development environment and folder structure.
Steps:
Install dependencies:

Create a folder structure:
city_simulator/
├── main.py
├── core/
│   ├── map.py
│   ├── building.py
│   ├── economy.py
├── assets/
│   ├── house.png
│   ├── factory.png
│   ├── park.png
├── data/
│   ├── save.json
├── ui/
│   ├── hud.py
│   ├── menu.py
├── utils/
│   ├── constants.py
├── README.md
🏗️ 2. Map & Basic Rendering (3–4 hours)
🎯 Goal:
Create the grid (e.g., 10×10) where the player can build structures.
Tasks:
Implement CityMap class:
Stores the grid (list of lists).
Draws cells (arcade.draw_rectangle_filled).
Detects cell based on mouse position.
Create a Tile class:
class Tile:
    def __init__(self, x, y, type="empty"):
        self.x = x
        self.y = y
        self.type = type
Handle mouse clicks → build structure on selected tile.
Render the grid inside on_draw().
🏠 3. Building System (3–4 hours)
🎯 Goal:
Let the player construct different types of buildings.
Steps:
Create a Building class:
class Building:
    def __init__(self, name, cost, population_effect, happiness_effect):
        self.name = name
        self.cost = cost
        self.population_effect = population_effect
        self.happiness_effect = happiness_effect
Add basic building types:
House → increases population, low cost.
Factory → generates income, decreases happiness.
Park → increases happiness.
Link each building with an image from /assets.
💰 4. Economy & Simulation Logic (3–4 hours)
🎯 Goal:
Introduce economy, population, and happiness tracking.
Implement Economy class:
class Economy:
    def __init__(self):
        self.money = 1000
        self.population = 0
        self.happiness = 50

    def update(self, buildings):
        for b in buildings:
            self.population += b.population_effect
            self.happiness += b.happiness_effect
            self.money -= b.cost
Simulation loop (on_update()):
Tax collection.
Maintenance costs.
Happiness adjustments.
🕹️ 5. User Interface (HUD) (2–3 hours)
🎯 Goal:
Show player stats and add control buttons.
Features:
Display current money, population, happiness.
Buttons: “Build House”, “Build Factory”, “Build Park”.
“Next Turn” or automatic updates via on_update().
💡 Use arcade.gui.UIFlatButton or simple draw_text() labels.
💾 6. Save & Load System (2 hours)
🎯 Goal:
Allow saving and restoring game state.
Steps:
Save city data to JSON:
save_data = {
    "buildings": [(b.x, b.y, b.name) for b in buildings],
    "economy": vars(economy)
}
Load data at startup to restore progress.
📊 7. Analytics & Graphs (3–4 hours)
🎯 Goal:
Add a “Statistics” view with graphs.
Use matplotlib to visualize:
Population growth.
Budget changes.
Happiness trends.
(Optional) Store daily history in history.json.
⚡ 8. Simulation Events (3 hours)
🎯 Goal:
Make the city feel alive.
Each turn (week): simulate population growth, pollution, or migration.
Random events: “Factory breakdown”, “Energy shortage”, “Festival increases happiness”.
Time system: day/week/month progression.
🎨 9. Polish & Testing (2–3 hours)
🎯 Goal:
Make the simulator look professional and stable.
Tasks:
Add icons, start screen, or splash screen.
Balance gameplay (so resources aren’t infinite).
Create a clean README.md with screenshots.
Optional: add simple background music or sounds.
💼 10. Portfolio Preparation (1 hour)
🎯 Goal:
Prepare the project for presentation.
Include:
README.md with:
project description,
features,
screenshots,
setup instructions.
requirements.txt
Demo GIF or short video using OBS.
👥 Team Division (2 developers)
Developer 1	Developer 2
Simulation logic	Map rendering
Building & Economy classes	UI and buttons
Save/load & updates	Graphics and events
Testing balance	Graphs & analytics
⏱️ Estimated Time
Phase	Time
Setup & map	4h
Buildings & economy	6h
UI & simulation	6h
Save/load & graphs	5h
Polish & testing	4h
Total:	≈25 hours
🌟 Optional Improvements
AI City Advisor: Suggests actions (“Build a park to boost happiness”).
Pollution mechanics: Factories decrease happiness over time.
Achievements system: Milestones for population, money, etc.
Expandable map: Choose city size at start.