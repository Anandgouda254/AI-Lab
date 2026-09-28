def candidate_elimination(data):

    # Number of attributes
    num_attributes = len(data[0]) - 1

    # Initialize Specific and General boundaries
    S = ['0'] * num_attributes
    G = [['?'] * num_attributes]

    # Initialize S with the first positive example
    for row in data:
        if row[-1] == 'Yes':
            S = row[:-1].copy()
            break

    # Process each training example
    for row in data:

        # Separate attributes and class label
        inputs = row[:-1]
        label = row[-1]

        # -------------------------
        # Handle Positive Example
        # -------------------------
        if label == 'Yes':

            # Generalize S if required
            for i in range(num_attributes):

                if inputs[i] != S[i]:
                    S[i] = '?'

            # Remove hypotheses from G
            # that do not cover the positive example
            G = [
                g for g in G
                if all(
                    g[i] == '?' or g[i] == inputs[i]
                    for i in range(num_attributes)
                )
            ]

        # -------------------------
        # Handle Negative Example
        # -------------------------
        else:

            G_new = []

            for g in G:

                # Check whether G already rejects
                # the negative example
                if not all(
                    g[i] == '?' or g[i] == inputs[i]
                    for i in range(num_attributes)
                ):

                    # Already inconsistent with negative example
                    G_new.append(g)

                else:

                    # Specialize G
                    for i in range(num_attributes):

                        if g[i] == '?' and inputs[i] != S[i]:

                            # Create a copy of the hypothesis
                            g_candidate = g.copy()

                            # Specialize using S
                            g_candidate[i] = S[i]

                            # Avoid duplicate hypotheses
                            if g_candidate not in G_new:
                                G_new.append(g_candidate)

            # Update G
            G = G_new

    return S, G


# =====================================================
# MAIN PROGRAM
# =====================================================

if __name__ == "__main__":

    # Training Dataset
    dataset = [

        ['Sunny', 'Warm', 'Normal',
         'Strong', 'Warm', 'Same', 'Yes'],

        ['Sunny', 'Warm', 'High',
         'Strong', 'Warm', 'Same', 'Yes'],

        ['Rainy', 'Cold', 'High',
         'Strong', 'Warm', 'Change', 'No'],

        ['Sunny', 'Warm', 'High',
         'Strong', 'Cool', 'Change', 'Yes']
    ]

    # Call Candidate Elimination algorithm
    s_boundary, g_boundary = candidate_elimination(dataset)

    # Display Specific Boundary
    print("Specific Boundary (S):")
    print(s_boundary)

    # Display General Boundary
    print("\nGeneral Boundary (G):")

    for g in g_boundary:
        print(g)