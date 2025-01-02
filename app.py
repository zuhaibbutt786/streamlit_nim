import streamlit as st

# Initialize the game state
if "heap_sizes" not in st.session_state:
    st.session_state.heap_sizes = [3, 4, 5]

def minimax(heap_sizes, depth, is_maximizing):
    if sum(heap_sizes) == 0:
        return -1 if is_maximizing else 1

    if is_maximizing:
        best_score = float('-inf')
        for i in range(len(heap_sizes)):
            for take in range(1, heap_sizes[i] + 1):
                new_heaps = heap_sizes[:]
                new_heaps[i] -= take
                score = minimax(new_heaps, depth + 1, False)
                best_score = max(best_score, score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(len(heap_sizes)):
            for take in range(1, heap_sizes[i] + 1):
                new_heaps = heap_sizes[:]
                new_heaps[i] -= take
                score = minimax(new_heaps, depth + 1, True)
                best_score = min(best_score, score)
        return best_score

def best_move(heap_sizes):
    best_score = float('-inf')
    move = (0, 1)
    for i in range(len(heap_sizes)):
        for take in range(1, heap_sizes[i] + 1):
            new_heaps = heap_sizes[:]
            new_heaps[i] -= take
            score = minimax(new_heaps, 0, False)
            if score > best_score:
                best_score = score
                move = (i, take)
    return move

# Game interface
st.title("Nim Game with Minimax Algorithm")
st.subheader("Remove 1 or more items from a single heap. The player who removes the last item loses!")

# Display the heaps
for idx, size in enumerate(st.session_state.heap_sizes):
    st.write(f"Heap {idx + 1}: {'O' * size} ({size})")

# Player's turn
if sum(st.session_state.heap_sizes) > 0:
    st.subheader("Your Turn!")
    heap = st.selectbox("Select a heap:", options=[i + 1 for i, h in enumerate(st.session_state.heap_sizes) if h > 0])
    num_to_remove = st.slider(f"Number to remove from Heap {heap}:", 1, st.session_state.heap_sizes[heap - 1])

    if st.button("Make Move"):
        st.session_state.heap_sizes[heap - 1] -= num_to_remove
        st.session_state.turn = "computer" if st.session_state.turn == "player" else "player"


# Computer's turn
if sum(st.session_state.heap_sizes) > 0:
    st.subheader("Computer's Turn!")
    heap, take = best_move(st.session_state.heap_sizes)
    st.session_state.heap_sizes[heap] -= take
    st.write(f"Computer removed {take} from Heap {heap + 1}.")
    st.session_state.turn = "computer" if st.session_state.turn == "player" else "player"

# Game Over
if sum(st.session_state.heap_sizes) == 0:
    st.subheader("Game Over!")
    st.write("You win!" if len(st.session_state.heap_sizes) % 2 == 1 else "Computer wins!")
