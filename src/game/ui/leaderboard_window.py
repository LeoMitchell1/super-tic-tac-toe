from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QTableWidget, QTableWidgetItem, QHeaderView, 
                             QPushButton, QFrame)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor, QPalette
from game.data import database


class LeaderboardWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.database = database

        self.init_ui()
        self.load_leaderboard()
        
    def init_ui(self):
        self.setWindowTitle("Leaderboard")
        self.setMinimumSize(650, 750)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 20, 30, 30)
        main_layout.setSpacing(0)
        
        # Header container with border
        title_container = QFrame()
        title_container.setObjectName("titleContainer")
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 15)
        title_layout.setSpacing(5)
        
        title = QLabel("🏆 LEADERBOARD")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout.addWidget(title)
        
        subtitle = QLabel("Top 10 Players")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout.addWidget(subtitle)
        
        main_layout.addWidget(title_container)
        main_layout.addSpacing(20)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Rank", "Player", "Score"])
        
        # Table settings
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)  # Disable selection
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)  # Disable focus
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(False)
        
        # Column sizing
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(0, 90)
        self.table.setColumnWidth(2, 130)
        
        # Row height
        self.table.verticalHeader().setDefaultSectionSize(55)
        
        main_layout.addWidget(self.table)
        
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_layout.setSpacing(15)
        
        back_button = QPushButton("Back")
        back_button.setObjectName("backButton")
        back_button.clicked.connect(self.back_to_menu)
        back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        button_layout.addWidget(back_button)
        
        main_layout.addSpacing(20)
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
        
    def load_leaderboard(self):
        try:
            # Get leaderboard data
            leaderboard_data = self.database.get_leaderboard()
            
            # Clear existing rows
            self.table.setRowCount(0)
            
            # Check if leaderboard is empty
            if not leaderboard_data:
                # Show empty state message
                self.table.setRowCount(1)
                empty_message = QTableWidgetItem("No scores yet - be the first to play!")
                empty_message.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                empty_font = QFont()
                empty_font.setPointSize(14)
                empty_message.setFont(empty_font)
                empty_message.setForeground(QColor("#999999"))
                self.table.setSpan(0, 0, 1, 3)  # Merge all columns
                self.table.setItem(0, 0, empty_message)
                self.table.setRowHeight(0, 100)
                return
            
            # Populate table
            for rank, (name, score) in enumerate(leaderboard_data, start=1):
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                
                # Rank column
                rank_item = QTableWidgetItem(f"#{rank}")
                rank_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                rank_font = QFont()
                rank_font.setBold(True)
                rank_item.setFont(rank_font)
                
                # Special styling for top 3
                if rank == 1:
                    rank_item.setForeground(QColor("#FFD700"))  # Gold
                elif rank == 2:
                    rank_item.setForeground(QColor("#C0C0C0"))  # Silver
                elif rank == 3:
                    rank_item.setForeground(QColor("#CD7F32"))  # Bronze
                
                self.table.setItem(row_position, 0, rank_item)
                
                # Name column
                name_item = QTableWidgetItem(name)
                name_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                name_font = QFont()
                name_font.setPointSize(11)
                if rank <= 3:
                    name_font.setBold(True)
                name_item.setFont(name_font)
                self.table.setItem(row_position, 1, name_item)
                
                # Score column
                score_item = QTableWidgetItem(f"{score:,}")
                score_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                score_font = QFont()
                score_font.setPointSize(12)
                score_font.setBold(True)
                score_item.setFont(score_font)
                score_item.setForeground(QColor("#69c8ff"))
                self.table.setItem(row_position, 2, score_item)
                
        except Exception as e:
            print(f"Error loading leaderboard: {e}")

    def back_to_menu(self):
        from .menu_window import MenuWindow
        self.menu_window = MenuWindow()
        self.menu_window.show()
        self.close()