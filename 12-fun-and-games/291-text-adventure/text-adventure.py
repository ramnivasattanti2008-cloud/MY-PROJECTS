"""
Classic Text Adventure Game
Explore a mysterious castle, collect items, solve puzzles, and find the treasure!
"""

import sys
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Item:
    """Item that can be picked up or used."""
    name: str
    description: str
    takeable: bool = True


@dataclass
class Room:
    """A room in the game world."""
    name: str
    description: str
    items: list[Item] = field(default_factory=list)
    connections: dict[str, str] = field(default_factory=dict)  # direction -> room_id
    locked: bool = False
    required_item: Optional[str] = None
    puzzle_solved: bool = False
    visited: bool = False


class Game:
    """Main game class managing state and logic."""

    # ASCII Art
    TITLE_ART = r"""
    ╔══════════════════════════════════════════════════════════════════════╗
    ║                                                                      ║
    ║     ██████╗ ██╗   ██╗███╗   ██╗ ██████╗ ███████╗ ██████╗ ███╗   ██╗ ║
    ║     ██╔══██╗██║   ██║████╗  ██║██╔════╝ ██╔════╝██╔═══██╗████╗  ██║ ║
    ║     ██║  ██║██║   ██║██╔██╗ ██║██║  ███╗█████╗  ██║   ██║██╔██╗ ██║ ║
    ║     ██║  ██║██║   ██║██║╚██╗██║██║   ██║██╔══╝  ██║   ██║██║╚██╗██║ ║
    ║     ██████╔╝╚██████╔╝██║ ╚████║╚██████╔╝███████╗╚██████╔╝██║ ╚████║ ║
    ║     ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝ ║
    ║                    ████████╗██╗  ██╗███████╗                          ║
    ║                    ╚══██╔══╝██║  ██║██╔════╝                          ║
    ║                       ██║   ███████║█████╗                            ║
    ║                       ██║   ██╔══██║██╔══╝                            ║
    ║                       ██║   ██║  ██║███████╗                          ║
    ║                       ╚═╝   ╚═╝  ╚═╝╚══════╝                          ║
    ║                                                                      ║
    ╚══════════════════════════════════════════════════════════════════════╝
    """

    MAP_ART = r"""
                         ┌─────────────────────┐
                         │     CASTLE MAP      │
                         │                     │
    ┌──────────┐    ┌────┴────┐    ┌──────────┐
    │  ARMORY  │────│  HALL   │────│ LIBRARY  │
    └──────────┘    └────┬────┘    └──────────┘
                         │
              ┌──────────┼──────────┐
              │          │          │
        ┌─────┴────┐ ┌───┴───┐ ┌────┴─────┐
        │  DUNGEON │ │COURTYARD│ │TREASURY │
        └──────────┘ └───┬───┘ └──────────┘
                         │
                   ┌─────┴─────┐
                   │   GATE    │
                   └───────────┘
    """

    def __init__(self):
        self.rooms: dict[str, Room] = {}
        self.inventory: list[Item] = []
        self.current_room: str = "hall"
        self.game_over: bool = False
        self.won: bool = False
        self.moves: int = 0

        self._init_rooms()

    def _init_rooms(self):
        """Initialize all rooms in the castle."""

        # Hall (starting room)
        self.rooms["hall"] = Room(
            name="Grand Hall",
            description="You stand in a grand hall with faded tapestries on the walls. "
                       "A massive chandelier hangs overhead, its crystals catching the dim light. "
                       "Passages lead in all directions.",
            items=[Item("candle", "An old brass candle holder", True)],
            connections={"north": "armory", "south": "courtyard", "east": "library", "west": "hall"}
        )

        # Armory
        self.rooms["armory"] = Room(
            name="Armory",
            description="Racks of ancient weapons line the walls - swords, axes, and spears. "
                       "Most are rusted beyond use, but one gleaming sword catches your eye.",
            items=[
                Item("key", "A small iron key with strange markings", True),
                Item("sword", "A beautiful silver sword, still sharp", True)
            ],
            connections={"south": "hall"}
        )

        # Library
        self.rooms["library"] = Room(
            name="Ancient Library",
            description="Floor-to-ceiling bookshelves filled with dusty tomes. "
                       "A reading desk sits by a window, and a peculiar locked cabinet stands in the corner.",
            items=[Item("book", "A book titled 'Secrets of the Castle'", True)],
            connections={"west": "hall"},
            locked=True,
            required_item="key"
        )

        # Courtyard
        self.rooms["courtyard"] = Room(
            name="Castle Courtyard",
            description="An open courtyard with a dried-up fountain in the center. "
                       "Dead vines crawl up the walls. The castle gate lies to the south.",
            items=[],
            connections={"north": "hall", "south": "gate", "east": "treasury"}
        )

        # Dungeon
        self.rooms["dungeon"] = Room(
            name="Dark Dungeon",
            description="Cold, damp cells line the corridor. Chains hang from the walls. "
                       "Something glints in the corner of the farthest cell.",
            items=[Item("torch", "A still-burning torch", True)],
            connections={"west": "courtyard"}
        )

        # Treasury
        self.rooms["treasury"] = Room(
            name="Royal Treasury",
            description="Mountains of gold coins and precious gems glitter in the torchlight. "
                       "But the REAL treasure is a magnificent golden crown on a velvet pillow!",
            items=[Item("crown", "The Royal Crown of the Kingdom", True)],
            connections={"west": "courtyard"},
            locked=True,
            required_item="key"
        )

        # Gate
        self.rooms["gate"] = Room(
            name="Castle Gate",
            description="The massive iron gate stands here, with the dungeon entrance nearby. "
                       "Through the bars, you can see the forest beyond - and your way to freedom!",
            items=[],
            connections={"north": "courtyard", "down": "dungeon"}
        )

        # Secret Chamber (accessed from library)
        self.rooms["secret"] = Room(
            name="Secret Chamber",
            description="A hidden room filled with arcane artifacts! An ancient pedestal "
                       "holds a mysterious amulet.",
            items=[Item("amulet", "The Amulet of Power - your ticket to victory!", True)],
            connections={"south": "library"},
            puzzle_solved=False
        )

    def print_intro(self):
        """Print game introduction."""
        print("\033[96m" + self.TITLE_ART + "\033[0m")
        print("\033[93m" + """
    ═══════════════════════════════════════════════════════════════
                              HOW TO PLAY
    ═══════════════════════════════════════════════════════════════

    COMMANDS:
      look          - Examine your surroundings
      go <dir>      - Move in a direction (north, south, east, west, up, down)
      examine <item>- Look at an item more closely
      take <item>   - Pick up an item
      drop <item>   - Drop an item
      use <item>    - Use an item
      inventory     - Check your inventory
      map           - View the castle map
      help          - Show this help
      quit          - Exit the game

    YOUR GOAL: Find the Royal Crown and escape the castle!
    ═══════════════════════════════════════════════════════════════
        """ + "\033[0m")
        input("\n\033[92mPress ENTER to begin your adventure...\033[0m ")

    def print_map(self):
        """Print the ASCII map."""
        print("\033[94m" + self.MAP_ART + "\033[0m")
        print("\033[93mCurrent location: \033[1m" + self.rooms[self.current_room].name + "\033[0m")

    def look(self):
        """Look around the current room."""
        room = self.rooms[self.current_room]
        print("\n\033[1m\033[96m═══ " + room.name.upper() + " ═══\033[0m")
        print("\n" + room.description)

        if room.items:
            print("\n\033[93mYou see:\033[0m")
            for item in room.items:
                print(f"  - {item.name} ({item.description})")

        exits = ", ".join(room.connections.keys())
        print(f"\n\033[92mExits: {exits}\033[0m")

    def go_direction(self, direction: str):
        """Move to a connected room."""
        room = self.rooms[self.current_room]

        if direction not in room.connections:
            print(f"\033[91mYou can't go {direction} from here!\033[0m")
            return

        target_room_id = room.connections[direction]
        target_room = self.rooms[target_room_id]

        # Check if room is locked
        if target_room.locked:
            print(f"\033[91mThe way to {target_room.name} is locked!\033[0m")
            if target_room.required_item:
                print(f"\033[93mYou need a {target_room.required_item} to unlock it.\033[0m")
            return

        # Check for puzzle
        if target_room_id == "secret" and not room.puzzle_solved:
            if "book" in [i.name for i in self.inventory]:
                print("\033[93mThe book in your inventory glows! The secret passage opens!\033[0m")
                room.puzzle_solved = True
            else:
                print("\033[91mThis room seems to require something to open the passage...\033[0m")
                return

        self.current_room = target_room_id
        self.moves += 1
        room.visited = True
        self.look()

        # Check for victory condition
        if target_room_id == "gate" and "crown" in [i.name for i in self.inventory]:
            self.victory()

    def take_item(self, item_name: str):
        """Pick up an item."""
        room = self.rooms[self.current_room]

        for item in room.items:
            if item.name.lower() == item_name.lower():
                if not item.takeable:
                    print(f"\033[91mYou can't take the {item.name}.\033[0m")
                    return

                room.items.remove(item)
                self.inventory.append(item)
                print(f"\033[92mYou take the {item.name}.\033[0m")
                return

        print(f"\033[91mThere's no {item_name} here.\033[0m")

    def drop_item(self, item_name: str):
        """Drop an item."""
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                self.inventory.remove(item)
                self.rooms[self.current_room].items.append(item)
                print(f"\033[93mYou drop the {item.name}.\033[0m")
                return

        print(f"\033[91mYou don't have a {item_name}.\033[0m")

    def examine_item(self, item_name: str):
        """Examine an item in inventory or room."""
        # Check inventory first
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                print(f"\033[96m{item.name}:\033[0m {item.description}")
                return

        # Check room
        room = self.rooms[self.current_room]
        for item in room.items:
            if item.name.lower() == item_name.lower():
                print(f"\033[96m{item.name}:\033[0m {item.description}")
                return

        print(f"\033[91mYou don't see a {item_name}.\033[0m")

    def use_item(self, item_name: str):
        """Use an item in the current context."""
        item_found = None
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                item_found = item
                break

        if not item_found:
            print(f"\033[91mYou don't have a {item_name}.\033[0m")
            return

        # Handle specific item uses
        if item_name.lower() == "key":
            # Unlock locked rooms
            room = self.rooms[self.current_room]
            for direction, target_id in room.connections.items():
                target = self.rooms[target_id]
                if target.locked and target.required_item == "key":
                    target.locked = False
                    print(f"\033[92mYou unlock the door to {target.name}!\033[0m")
                    return
            print("There's nothing to unlock here.")

        elif item_name.lower() == "book":
            print("\033[96mYou read the book...\033[0m")
            print('"The secret chamber lies within the library, hidden from sight."')
            print('"Only those who carry this very book may reveal its entrance."')
            print("\033[93mThe book glows faintly!\033[0m")

        elif item_name.lower() == "torch":
            print("You hold up the torch, illuminating the darkness.")

        elif item_name.lower() == "sword":
            print("You swing the silver sword through the air. It feels powerful!")

        elif item_name.lower() == "candle":
            print("The candle flickers, casting dancing shadows on the walls.")

        elif item_name.lower() == "amulet":
            print("\033[95mThe Amulet of Power pulses with magical energy!\033[0m")
            print("It seems to be waiting for something...")

        elif item_name.lower() == "crown":
            print("\033[95mThe Royal Crown! This is what you came for!\033[0m")
            if self.current_room == "gate":
                print("\033[92mWith the crown, you can now escape through the gate!\033[0m")

        else:
            print(f"You're not sure how to use the {item_name} here.")

    def show_inventory(self):
        """Show inventory contents."""
        if not self.inventory:
            print("\033[93mYour inventory is empty.\033[0m")
            return

        print("\n\033[96m═══ INVENTORY ═══\033[0m")
        for item in self.inventory:
            print(f"  - {item.name}")
        print()

    def victory(self):
        """Handle winning the game."""
        self.won = True
        self.game_over = True
        print("\n" + "\033[92m" + """
    ╔════════════════════════════════════════════════════════════════╗
    ║                                                                ║
    ║     ███╗   ██╗██╗ ██████╗ ██╗  ██╗████████╗███████╗ █████╗ ██╗   ║
    ║     ████╗  ██║██║██╔════╝ ██║  ██║╚══██╔══╝██╔════╝██╔══██╗██║   ║
    ║     ██╔██╗ ██║██║██║  ███╗███████║   ██║   █████╗  ███████║██║   ║
    ║     ██║╚██╗██║██║██║   ██║██╔══██║   ██║   ██╔══╝  ██╔══██║██║   ║
    ║     ██║ ╚████║██║╚██████╔╝██║  ██║   ██║   ██║     ██║  ██║███████╗
    ║     ╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚═╝  ╚═╝╚═════╝
    ║                                                                ║
    ╚════════════════════════════════════════════════════════════════╝
        """ + "\033[0m")
        print(f"\033[93mYou escaped the castle with the Royal Crown!\033[0m")
        print(f"\nCongratulations! You completed the game in \033[96m{self.moves}\033[0m moves.")
        print("\nThank you for playing Castle Quest!")
        print("\n\033[96mFinal Inventory:\033[0m")
        for item in self.inventory:
            print(f"  - {item.name}")

    def process_command(self, command: str):
        """Process player input."""
        parts = command.lower().strip().split()
        if not parts:
            return

        cmd = parts[0]

        if cmd in ("n", "north"):
            self.go_direction("north")
        elif cmd in ("s", "south"):
            self.go_direction("south")
        elif cmd in ("e", "east"):
            self.go_direction("east")
        elif cmd in ("w", "west"):
            self.go_direction("west")
        elif cmd in ("u", "up"):
            self.go_direction("up")
        elif cmd in ("d", "down"):
            self.go_direction("down")
        elif cmd == "go" and len(parts) > 1:
            self.go_direction(parts[1])
        elif cmd == "look" or cmd == "l":
            self.look()
        elif cmd == "examine" or cmd == "x":
            if len(parts) > 1:
                self.examine_item(" ".join(parts[1:]))
            else:
                print("Examine what?")
        elif cmd == "take" or cmd == "get" or cmd == "grab":
            if len(parts) > 1:
                self.take_item(" ".join(parts[1:]))
            else:
                print("Take what?")
        elif cmd == "drop":
            if len(parts) > 1:
                self.drop_item(" ".join(parts[1:]))
            else:
                print("Drop what?")
        elif cmd == "use":
            if len(parts) > 1:
                self.use_item(" ".join(parts[1:]))
            else:
                print("Use what?")
        elif cmd == "inventory" or cmd == "i" or cmd == "inv":
            self.show_inventory()
        elif cmd == "map" or cmd == "m":
            self.print_map()
        elif cmd == "help" or cmd == "h" or cmd == "?":
            self.show_help()
        elif cmd == "quit" or cmd == "exit" or cmd == "q":
            print("\n\033[93mThanks for playing Castle Quest!\033[0m")
            print("Better luck next time...")
            self.game_over = True
        else:
            print(f"\033[91mI don't understand '{command}'. Type 'help' for commands.\033[0m")

    def show_help(self):
        """Show help text."""
        print("""
\033[96m═══ AVAILABLE COMMANDS ═══\033[0m

  Movement: north/n, south/s, east/e, west/w, up/u, down/d
            go <direction>

  Actions:  look/l     - Look around the room
            examine/x   - Examine an item
            take/get   - Pick up an item
            drop       - Drop an item
            use        - Use an item
            inventory/i - Show your items

  Other:    map/m      - View the castle map
            help/h     - Show this help
            quit/q     - Exit the game

\033[93mTIP:\033[0m Examine everything! Some items might be more useful than they appear.
        """)

    def run(self):
        """Main game loop."""
        self.print_intro()
        self.look()

        while not self.game_over:
            print()
            cmd = input("\033[94m>\033[0m ").strip()
            if cmd:
                self.process_command(cmd)


def main():
    """Entry point."""
    print("\033[2J\033[H")  # Clear screen
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
