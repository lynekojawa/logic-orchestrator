# 4/16: Determinant calculator begin, goal is building a determinant calculator and eventually get UI
# ... many new tool detected. @property, defining class then under the class defining functions.
# For any project phase 1 is the hardest ugh!
class Matrix:
    def __init__(self, matrix_data):
        row_length = [len(row) for row in matrix_data]
        if len(set(row_length)) > 1:
            raise ValueError("All rows must have the same number of columns")

        self.matrix = matrix_data

    def __repr__(self):
        if not self.matrix:
            return "[ ]"
        return "\n".join([f"[{','.join(map(str, row))}]" for row in self.matrix])

    def get_row(self, index):
        return self.matrix[index]

    def get_col(self, index):
        return [row[index] for row in self.matrix]

    @property
    def shape(self):
        rows = len(self.matrix)
        cols = len(self.matrix[0]) if rows > 0 else 0
        return rows, cols

    @property
    def is_square(self):
        n, m = self.shape
        return n == m

    def det_base(self):
        n, m = self.shape

        if not self.is_square:
            raise ValueError("Determinant can only be calculated for a Square matrix!")

        if n == 1:
            return self.matrix[0][0]
        elif n == 2:
            return (self.matrix[0][0] * self.matrix[1][1]) - (self.matrix[0][1] * self.matrix[1][0])
        else:
            raise ValueError("In Progress... Laplace expansion coming soon! :D")


# --- Test Strike Zone ---
if __name__ == "__main__":
    print("=== Test v1.0 ===")
    try:
        n = int(input("Enter the number of Rows (n): "))
        m = int(input("Enter the number of Columns (m): "))

        print(f"Enter each row's elements separated by spaces (e.g, '1 2 3':")

        user_matrix_data = []
        for i in range(n):
            row_input = input(f"Row {i + 1}: ")
            row_data = list(map(float, row_input.split()))
            user_matrix_data.append(row_data)

        emp_matrix = Matrix(user_matrix_data)


        print("\n--- Ingested Matrix ---")
        print(emp_matrix)
        print(f"Shape: {emp_matrix.shape}")

        if emp_matrix.is_square:
            print(f"Determinant: {emp_matrix.det_base()}")
        else:
            print("Notice: This is not a Square Matrix. Determinant is undefined.")

    except ValueError as e:
        print(f"Critical Input Error: {e}")
