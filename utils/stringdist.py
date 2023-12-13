# A simple string distance calculator.

# Since chatterino-summary is meant to be used with minimal effort from 
# a nontechnical user, I don't want to require them to install a
# dependency to calculate the string distance between two strings.
# So, here is a simple implementation of the Levenshtein distance calculator.

def print_distances(distances: list, string1: str, string2: str) -> None:
    # Print the distance matrix in a readable format.
    for s1 in range(len(string1) + 1):
        for s2 in range(len(string2) + 1):
            print(int(distances[s1][s2]), end=" ")
        print()

def dist(string1: str, string2: str) -> float:
    # Calculate the Levenshtein distance between two strings.

    # Convert both strings to lowercase.
    string1 = string1.lower()
    string2 = string2.lower()

    m = len(string1)
    n = len(string2)

    # Create a matrix of size m+1 x n+1
    distance_matrix = [[0 for x in range(n+1)] for x in range(m+1)]
    for t1 in range(m + 1):
        distance_matrix[t1][0] = t1
    for t2 in range(n + 1):
        distance_matrix[0][t2] = t2
    
    a = 0
    b = 0
    c = 0

    for s1 in range(1, len(string1) + 1):
        for s2 in range(1, len(string2) + 1):
            if string1[s1-1] == string2[s2-1]:
                distance_matrix[s1][s2] = distance_matrix[s1-1][s2-1]
            else:
                a = distance_matrix[s1][s2-1]
                b = distance_matrix[s1-1][s2]
                c = distance_matrix[s1-1][s2-1]

                if a <= b and a <= c:
                    distance_matrix[s1][s2] = a + 1
                elif b <= a and b <= c:
                    distance_matrix[s1][s2] = b + 1
                else:
                    distance_matrix[s1][s2] = c + 1

    # print_distances(distance_matrix, string1, string2)

    return distance_matrix[m][n]


if __name__ == "__main__":
    print(dist("diraction", "direction"))