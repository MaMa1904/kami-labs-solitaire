import random

def get_card_name(card_num):
    """Convert card number (0-31) to readable name."""
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
    
    suit_index = card_num // 8
    rank_index = card_num % 8
    
    return f"{ranks[rank_index]} of {suits[suit_index]}"

def get_suit(card_num):
    """Return the suit index (0-3) for a card."""
    return card_num // 8

def display_table(table):
    """Display the four table positions in 2x2 format."""
    line1 = f"    {get_card_name(table[0])} {get_card_name(table[1])}"
    line2 = f"    {get_card_name(table[2])} {get_card_name(table[3])}"
    print(line1)
    print(line2)

def count_suits(table):
    """Count how many cards of each suit are on the table."""
    suit_counts = [0, 0, 0, 0]
    for card in table:
        if card is not None:
            suit_counts[get_suit(card)] += 1
    return suit_counts

def play_game(seed):
    """Play one game of solitaire with the given seed."""
    random.seed(seed)
    cards = list(range(32))
    random.shuffle(cards)
    
    # Deal first 4 cards
    table = [cards.pop(0) for _ in range(4)]
    
    print()
    display_table(table)
    
    while True:
        # Check lose condition first: all four suits on table with cards remaining
        suit_counts = count_suits(table)
        if all(count >= 1 for count in suit_counts) and len(cards) > 0:
            print()
            print("LOSE")
            return len(cards)
        
        # Count suits for removal logic
        suits_on_table = []
        for i in range(4):
            suits_on_table.append(get_suit(table[i]))
        
        # Count how many of each suit
        suit_positions = {0: [], 1: [], 2: [], 3: []}
        for pos in range(4):
            suit = suits_on_table[pos]
            suit_positions[suit].append(pos)
        
        # Determine which cards to remove
        to_remove = []
        
        # Count how many suits have multiple cards
        suits_with_multiple = [suit for suit, positions in suit_positions.items() if len(positions) >= 2]
        
        if len(suits_with_multiple) == 2:
            # Two pairs of matching suits - remove all four
            for suit in suits_with_multiple:
                to_remove.extend(suit_positions[suit])
        elif len(suits_with_multiple) == 1:
            # One suit with multiple cards
            suit = suits_with_multiple[0]
            positions = suit_positions[suit]
            if len(positions) == 4:
                # All four cards same suit - remove all four
                to_remove = positions
            elif len(positions) == 3:
                # Three of a suit - remove the two in lower positions
                positions_sorted = sorted(positions)
                to_remove = positions_sorted[:2]
            elif len(positions) == 2:
                # Exactly two cards share a suit - remove them
                to_remove = positions
        
        # If no cards to remove, we're stuck (shouldn't happen with proper logic)
        if not to_remove:
            # This means all four suits are different - will be caught by lose condition
            continue
        
        # Remove the cards (set to None)
        for pos in to_remove:
            table[pos] = None
        
        # Refill from deck - always fill lowest-numbered empty position first
        for pos in range(4):
            if table[pos] is None and len(cards) > 0:
                table[pos] = cards.pop(0)
        
        # Check win condition after refilling: deck is empty
        if len(cards) == 0:
            print()
            print("WIN")
            return 0
        
        # Display the new table state only if all positions are filled
        print()
        display_table(table)

def simulate(n, i):
    """Simulate n games starting with seed i."""
    results = {}
    
    for seed in range(i, i + n):
        random.seed(seed)
        cards = list(range(32))
        random.shuffle(cards)
        
        # Deal first 4 cards
        table = [cards.pop(0) for _ in range(4)]
        
        while True:
            # Check lose condition first: all four suits on table with cards remaining
            suit_counts = count_suits(table)
            if all(count >= 1 for count in suit_counts) and len(cards) > 0:
                cards_left = len(cards)
                break
            
            # Count suits for removal logic
            suits_on_table = []
            for j in range(4):
                suits_on_table.append(get_suit(table[j]))
            
            # Count how many of each suit
            suit_positions = {0: [], 1: [], 2: [], 3: []}
            for pos in range(4):
                suit = suits_on_table[pos]
                suit_positions[suit].append(pos)
            
            # Determine which cards to remove
            to_remove = []
            
            # Count how many suits have multiple cards
            suits_with_multiple = [suit for suit, positions in suit_positions.items() if len(positions) >= 2]
            
            if len(suits_with_multiple) == 2:
                # Two pairs of matching suits - remove all four
                for suit in suits_with_multiple:
                    to_remove.extend(suit_positions[suit])
            elif len(suits_with_multiple) == 1:
                # One suit with multiple cards
                suit = suits_with_multiple[0]
                positions = suit_positions[suit]
                if len(positions) == 4:
                    # All four cards same suit - remove all four
                    to_remove = positions
                elif len(positions) == 3:
                    # Three of a suit - remove the two in lower positions
                    positions_sorted = sorted(positions)
                    to_remove = positions_sorted[:2]
                elif len(positions) == 2:
                    # Exactly two cards share a suit - remove them
                    to_remove = positions
            
            # Remove the cards (set to None)
            for pos in to_remove:
                table[pos] = None
            
            # Refill from deck - always fill lowest-numbered empty position first
            for pos in range(4):
                if table[pos] is None and len(cards) > 0:
                    table[pos] = cards.pop(0)
            
            # Check win condition after refilling: deck is empty
            if len(cards) == 0:
                cards_left = 0
                break
        
        # Record the result
        if cards_left not in results:
            results[cards_left] = 0
        results[cards_left] += 1
    
    # Print the results
    for cards_left in sorted(results.keys()):
        percentage = (results[cards_left] / n) * 100
        if percentage > 0:
            print(f"{cards_left} cards left: {percentage:.2f}%")

def main():
    """Main function to run the solitaire game."""
    seed_input = input("Enter an integer to pass to the seed() function: ")
    seed = int(seed_input)
    play_game(seed)

if __name__ == "__main__":
    main()