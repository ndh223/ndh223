// tictactoe.cpp
// Tro choi caro 3x3 (Tic-Tac-Toe) console, Nguoi vs Nguoi hoac Nguoi vs May (Minimax).
// Bien dich: g++ -std=c++17 -O2 tictactoe.cpp -o tictactoe

#include <iostream>
#include <vector>
#include <limits>
using namespace std;

enum class Cell { Empty=' ', X='X', O='O' };

struct Board {
    vector<Cell> c;
    Board() : c(9, Cell::Empty) {}
    void display() const {
        cout << "\n";
        for (int i = 0; i < 9; i += 3) {
            cout << " " << char(c[i])   << " | " << char(c[i+1]) << " | " << char(c[i+2]) << "    "
                 << i+1 << " | " << i+2 << " | " << i+3 << "\n";
            if (i < 6) cout << "---+---+---    ---+---+---\n";
        }
        cout << "\n";
    }
    bool isFull() const {
        for (auto &x: c) if (x == Cell::Empty) return false;
        return true;
    }
    Cell checkWin() const {
        const int wins[8][3] = {
            {0,1,2},{3,4,5},{6,7,8},
            {0,3,6},{1,4,7},{2,5,8},
            {0,4,8},{2,4,6}
        };
        for (auto &w : wins) {
            if (c[w[0]] != Cell::Empty && c[w[0]] == c[w[1]] && c[w[1]] == c[w[2]])
                return c[w[0]];
        }
        return Cell::Empty;
    }
};

int scoreFor(Cell winner, Cell aiPlayer, Cell human) {
    if (winner == aiPlayer) return +10;
    if (winner == human)   return -10;
    return 0;
}

pair<int,int> minimax(Board board, Cell currentPlayer, Cell aiPlayer, Cell human, int depth=0) {
    Cell winner = board.checkWin();
    if (winner != Cell::Empty || board.isFull()) {
        int s = scoreFor(winner, aiPlayer, human);
        if (s > 0) s -= depth;
        if (s < 0) s += depth;
        return {s, -1};
    }
    vector<int> moves;
    for (int i=0;i<9;i++) if (board.c[i] == Cell::Empty) moves.push_back(i);

    int bestScore = (currentPlayer == aiPlayer) ? numeric_limits<int>::min() : numeric_limits<int>::max();
    int bestMove = -1;

    for (int m : moves) {
        board.c[m] = currentPlayer;
        auto [s, mm] = minimax(board, (currentPlayer==Cell::X?Cell::O:Cell::X), aiPlayer, human, depth+1);
        board.c[m] = Cell::Empty;

        if (currentPlayer == aiPlayer) {
            if (s > bestScore) { bestScore = s; bestMove = m; }
        } else {
            if (s < bestScore) { bestScore = s; bestMove = m; }
        }
    }
    return {bestScore, bestMove};
}

int getHumanMove(const Board &board) {
    while (true) {
        cout << "Chon o (1-9): ";
        int pos;
        if (!(cin >> pos)) {
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            cout << "Nhap sai. Thu lai.\n";
            continue;
        }
        if (pos < 1 || pos > 9) {
            cout << "So khong hop le. Nhap 1..9.\n";
            continue;
        }
        if (board.c[pos-1] != Cell::Empty) {
            cout << "O da duoc danh. Chon o khac.\n";
            continue;
        }
        return pos-1;
    }
}

int main() {
    cout << "=== TRO CHOI TIC TAC TOE ===\n";
    cout << "1. Che do 1 nguoi (choi voi may)\n2. Che do 2 nguoi\nLua chon: ";
    int mode;
    while (!(cin >> mode) || (mode != 1 && mode != 2)) {
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
        cout << "Chon 1 hoac 2: ";
    }

    Board board;
    Cell human = Cell::X, ai = Cell::O;
    bool humanStarts = true;

    if (mode == 1) {
        cout << "Ban muon danh X hay O? (X di truoc): X/O : ";
        char ch;
        while (true) {
            cin >> ch;
            if (ch == 'X' || ch == 'x') { human = Cell::X; ai = Cell::O; humanStarts = true; break; }
            if (ch == 'O' || ch == 'o') { human = Cell::O; ai = Cell::X; humanStarts = false; break; }
            cout << "Nhap X hoac O: ";
        }
    }

    Cell turn = Cell::X;
    board.display();

    while (true) {
        Cell winner = board.checkWin();
        if (winner != Cell::Empty) {
            cout << "Ket qua: ";
            if (winner == human && mode==1) cout << "Ban thang!\n";
            else if (mode==1) cout << "May thang!\n";
            else cout << "Nguoi choi " << char(winner) << " thang!\n";
            cout << "Game Over\n";
            break;
        }
        if (board.isFull()) {
            cout << "Hoa!\nGame Over\n";
            break;
        }

        if (mode == 2) {
            cout << "Luot cua " << char(turn) << "\n";
            int mv = getHumanMove(board);
            board.c[mv] = turn;
        } else {
            if (turn == human) {
                cout << "Luot cua ban (" << char(human) << ")\n";
                int mv = getHumanMove(board);
                board.c[mv] = human;
            } else {
                cout << "Luot cua may (" << char(ai) << ") dang tinh...\n";
                auto res = minimax(board, ai, ai, human);
                int mv = res.second;
                if (mv == -1) {
                    for (int i=0;i<9;i++) if (board.c[i] == Cell::Empty) { mv=i; break; }
                }
                board.c[mv] = ai;
                cout << "May danh o " << (mv+1) << "\n";
            }
        }

        board.display();
        turn = (turn == Cell::X) ? Cell::O : Cell::X;
    }

    cout << "Cam on da choi!\n";
    return 0;
}
