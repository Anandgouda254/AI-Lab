class MeansEndAnalysis:
    def __init__(self, operators):
        self.operators = operators

    def solve(self, current, goal):
        plan = []

        print(f"Current State: {current} | Goal State: {goal}")

        # Check whether goal is already achieved
        if self.goal_satisfied(current, goal):
            return plan

        # Find the difference
        diff = self.find_difference(current, goal)

        if not diff:
            return None

        # Select operator to solve the difference
        op = self.select_operator(diff)

        if not op:
            print(f"No operator found to resolve difference: {diff}")
            return None

        # Achieve all preconditions
        for key, value in op['precond'].items():

            if current.get(key) != value:
                subgoal = {key: value}

                print(f"Subgoal: {subgoal}")

                subplan = self.solve(current, subgoal)

                if subplan is None:
                    return None

                plan.extend(subplan)

        # Apply the selected operator
        print(f"Applying Operator: {op['name']}")

        current.update(op['effect'])
        plan.append(op['name'])

        # Check whether final goal is achieved
        if self.goal_satisfied(current, goal):
            return plan

        # Continue solving
        remaining_plan = self.solve(current, goal)

        if remaining_plan is None:
            return None

        plan.extend(remaining_plan)

        return plan

    def goal_satisfied(self, current, goal):
        for key, value in goal.items():
            if current.get(key) != value:
                return False
        return True

    def find_difference(self, current, goal):
        for key, value in goal.items():
            if current.get(key) != value:
                return (key, value)
        return None

    def select_operator(self, diff):
        key, value = diff

        for op in self.operators:
            if op['effect'].get(key) == value:
                return op

        return None


# Example Usage
if __name__ == "__main__":

    operators = [
        {
            'name': 'Drive_Car',
            'precond': {
                'has_car': True,
                'at_home': True
            },
            'effect': {
                'at_work': True,
                'at_home': False
            }
        },

        {
            'name': 'Buy_Car',
            'precond': {
                'has_money': True,
                'has_car': False
            },
            'effect': {
                'has_car': True
            }
        }
    ]

    current_state = {
        'has_money': True,
        'has_car': False,
        'at_home': True,
        'at_work': False
    }

    goal_state = {
        'at_work': True
    }

    mea = MeansEndAnalysis(operators)

    plan = mea.solve(current_state, goal_state)

    print("\nExecution Plan:", plan)