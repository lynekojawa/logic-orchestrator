# 4/17 today we are getting into phase 2 of the determinant calculator.
#spend some time why can we calculate determinant in square matrix and because we need to get AA^-1 = I
#the sign of determinant means + moved exactly same - moved in mirror, and how much it get larger in terms of the area or volume
#deleted get_base function, it is merged into determinant_calculator since it handles all, and saving some lines.
# Adding a feature for GLn(Fq) to determine determinant. also wanted to add matrix squares with finite field.

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

#phase 2 function
    def get_minor(self, row_idx, col_idx):
        n, m = self.shape
        sub_data = [
            [self.matrix[r][c] for c in range(m) if c != col_idx]
            for r in range(n) if r != row_idx
        ]

        return Matrix(sub_data)

    def calculate_determinant(self, mod=None):
        if not self.is_square:
            raise ValueError("Determinant can only be calculated for a Square matrix!")

        n,m = self.shape
        res = 0
        if n == 1:
            return self.matrix[0][0]
        elif n == 2:
            return (self.matrix[0][0] * self.matrix[1][1]) - (self.matrix[0][1] * self.matrix[1][0])

        else:
            total_det = 0
            for j in range(m):
                sign = 1 if j %2 ==0 else -1
                minor = self.get_minor(0,j)

                sub_det = minor.calculate_determinant(mod)
                total_det += sign * self.matrix[0][j] * sub_det
            res = total_det
        if mod is not None:
            return res % mod
        return res

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
            print(f"Standard Determinant: {emp_matrix.calculate_determinant()}")
            print(f"Determinant in F2: {emp_matrix.calculate_determinant(mod=2)} ")
        else:
            print("Notice: This is not a Square Matrix. Determinant is undefined.")

    except ValueError as e:
        print(f"Critical Input Error: {e}")
