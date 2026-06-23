from models import AirQualityRecord


class RiskAnalyzer:

    @staticmethod
    def classify(record: AirQualityRecord) -> AirQualityRecord:
        risk_scores = [
            RiskAnalyzer._pm25_risk(record.pm25),
            RiskAnalyzer._pm10_risk(record.pm10),
            RiskAnalyzer._nitrogen_dioxide_risk(record.nitrogen_dioxide),
            RiskAnalyzer._ozone_risk(record.ozone),
            RiskAnalyzer._sulphur_dioxide_risk(record.sulphur_dioxide),
        ]

        final_score = max(risk_scores)

        record.risk_level = RiskAnalyzer._risk_label(final_score)
        record.recommendation = RiskAnalyzer._recommendation(
            record.risk_level
        )

        return record

    @staticmethod
    def _pm25_risk(value):
        if value is None:
            return 0
        if value <= 5:
            return 1
        if value <= 15:
            return 2
        if value <= 50:
            return 3
        return 4

    @staticmethod
    def _pm10_risk(value):
        if value is None:
            return 0
        if value <= 15:
            return 1
        if value <= 45:
            return 2
        if value <= 120:
            return 3
        return 4

    @staticmethod
    def _nitrogen_dioxide_risk(value):
        if value is None:
            return 0
        if value <= 10:
            return 1
        if value <= 25:
            return 2
        if value <= 60:
            return 3
        return 4

    @staticmethod
    def _ozone_risk(value):
        if value is None:
            return 0
        if value <= 60:
            return 1
        if value <= 100:
            return 2
        if value <= 120:
            return 3
        return 4

    @staticmethod
    def _sulphur_dioxide_risk(value):
        if value is None:
            return 0
        if value <= 20:
            return 1
        if value <= 40:
            return 2
        if value <= 125:
            return 3
        return 4

    @staticmethod
    def _risk_label(score):
        labels = {
            0: "Unknown",
            1: "Low",
            2: "Moderate",
            3: "High",
            4: "Very High",
        }

        return labels.get(score, "Unknown")

    @staticmethod
    def _recommendation(risk_level):
        recommendations = {
            "Low": "Outdoor activity is generally suitable.",
            "Moderate": (
                "Outdoor activity is acceptable, but sensitive users "
                "should reduce prolonged exposure."
            ),
            "High": (
                "Reduce intense outdoor activity, especially for children, "
                "elderly people, and users with respiratory conditions."
            ),
            "Very High": (
                "Avoid intense outdoor activity. Sensitive users should "
                "consider staying indoors."
            ),
            "Unknown": "Not enough data is available to provide advice.",
        }

        return recommendations.get(
            risk_level,
            recommendations["Unknown"],
        )