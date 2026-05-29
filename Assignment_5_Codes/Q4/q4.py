from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination


# =====================================================
# CREATE BAYESIAN NETWORK
# =====================================================

model = DiscreteBayesianNetwork([
    ("Burglary", "Alarm"),
    ("Earthquake", "Alarm"),
    ("Alarm", "JohnCalls"),
    ("Alarm", "MaryCalls")
])


# =====================================================
# DEFINE PROBABILITY TABLES (CPDs)
# =====================================================

# P(Burglary)
cpd_burglary = TabularCPD(
    variable="Burglary",
    variable_card=2,
    values=[[0.999],
            [0.001]]
)

# P(Earthquake)
cpd_earthquake = TabularCPD(
    variable="Earthquake",
    variable_card=2,
    values=[[0.998],
            [0.002]]
)

# P(Alarm | Burglary, Earthquake)
cpd_alarm = TabularCPD(
    variable="Alarm",
    variable_card=2,
    values=[
        [0.999, 0.06, 0.71, 0.05],
        [0.001, 0.94, 0.29, 0.95]
    ],
    evidence=["Burglary", "Earthquake"],
    evidence_card=[2, 2]
)

# P(JohnCalls | Alarm)
cpd_john = TabularCPD(
    variable="JohnCalls",
    variable_card=2,
    values=[
        [0.95, 0.10],
        [0.05, 0.90]
    ],
    evidence=["Alarm"],
    evidence_card=[2]
)

# P(MaryCalls | Alarm)
cpd_mary = TabularCPD(
    variable="MaryCalls",
    variable_card=2,
    values=[
        [0.99, 0.30],
        [0.01, 0.70]
    ],
    evidence=["Alarm"],
    evidence_card=[2]
)


# =====================================================
# ADD CPDs TO NETWORK
# =====================================================

model.add_cpds(
    cpd_burglary,
    cpd_earthquake,
    cpd_alarm,
    cpd_john,
    cpd_mary
)

# Verify model correctness
print("Model Valid:", model.check_model())


# =====================================================
# INFERENCE
# =====================================================

inference = VariableElimination(model)

# Query:
# Probability of burglary given both John and Mary called

result = inference.query(
    variables=["Burglary"],
    evidence={
        "JohnCalls": 1,
        "MaryCalls": 1
    }
)

print("\nProbability of Burglary given John and Mary called:")
print(result)


# =====================================================
# ADDITIONAL QUERIES
# =====================================================

alarm_prob = inference.query(
    variables=["Alarm"]
)

print("\nProbability of Alarm:")
print(alarm_prob)

earthquake_prob = inference.query(
    variables=["Earthquake"],
    evidence={
        "JohnCalls": 1
    }
)

print("\nProbability of Earthquake given John called:")
print(earthquake_prob)
