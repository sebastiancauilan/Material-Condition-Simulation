import random

# -----------------------------
# CONFIG
# -----------------------------
NUM_AGENTS = 100
YEARS = 5

# -----------------------------
# AGENT CLASS
# -----------------------------
class Person:
    def __init__(self, name):
        self.name = name
        self.education = random.uniform(0.5, 1)   # normalized
        self.parent_income = random.uniform(20000, 150000)
        self.annual_wage = self.assign_initial_wealth()
        self.wealth = self.annual_wage + 0.1 * self.parent_income  # start wealth

        self.quality_of_life = self.calculate_qol()
        self.support_socialist = self.calculate_support()

    def assign_initial_wealth(self):
        """Assign initial wage/wealth based on population distribution"""
        rand = random.random()  # 0-1
        if rand < 0.01:  # top 1%
            return random.uniform(1_000_000_000, 10_000_000_000)
        elif rand < 0.41:  # next 40%
            return random.uniform(100_000, 999_999)
        else:  # remaining 59%
            return random.uniform(0, 99_999)

    def calculate_qol(self):
        """Quality of life weighted by wealth, education, and parental income"""
        normalized_wealth = min(self.wealth / 1_000_000_000, 1)  # normalize to 0-1
        normalized_parent = min(self.parent_income / 200_000, 1)
        return 0.5 * normalized_wealth + 0.3 * self.education + 0.2 * normalized_parent

    def calculate_support(self):
        """Probability of supporting socialist policies inversely related to QoL"""
        base_support = 1 - self.quality_of_life
        return min(max(base_support + random.uniform(-0.05, 0.05), 0), 1)

    def update_year(self):
        """Simulate one year: change wages, wealth, recalc QoL and support"""
        # Random wage fluctuation
        self.annual_wage += random.uniform(-5000, 5000)
        self.annual_wage = max(self.annual_wage, 0)

        # Wealth accumulates from wage + small parental contribution
        self.wealth += self.annual_wage + 0.05 * self.parent_income

        # Recalculate QoL and support
        self.quality_of_life = self.calculate_qol()
        self.support_socialist = self.calculate_support()


# -----------------------------
# INITIALIZE AGENTS
# -----------------------------
agents = [Person(f"Person_{i+1}") for i in range(NUM_AGENTS)]

# -----------------------------
# SIMULATION LOOP (YEARLY)
# -----------------------------
for year in range(1, YEARS + 1):
    print(f"\n--- Year {year} ---")

    for agent in agents:
        agent.update_year()

    # Global average support
    avg_support = sum(agent.support_socialist for agent in agents) / NUM_AGENTS
    print(f"Average socialist support: {avg_support*100:.2f}%")

    # Optional: print each agent's details
    for agent in agents:
        print(f"{agent.name}: Wealth=${agent.wealth:,.2f}, QoL={agent.quality_of_life:.3f}, Socialist Support={agent.support_socialist:.3f}")
