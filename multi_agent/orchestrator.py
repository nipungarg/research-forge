from multi_agent.writer import WriterAgent
from multi_agent.editor import EditorAgent


class Orchestrator:
    def __init__(self, max_iterations=3):
        self.writer = WriterAgent()
        self.editor = EditorAgent()
        self.max_iterations = max_iterations

    def should_stop_early(self, review, iteration):
        # Stop if no issues
        if review["is_approved"]:
            return True

        # Stop if no meaningful feedback
        if not review["issues"] and not review["missing_points"]:
            return True

        # Prevent over-iteration
        if iteration >= self.max_iterations - 1:
            return True

        return False

    def run(self, researcher_output):
        feedback = None
        prev_issues = None

        for i in range(self.max_iterations):
            print(f"\n--- Iteration {i + 1} ---")

            writer_output = self.writer.run(
                researcher_output,
                feedback
            )

            review = self.editor.run(writer_output)

            print("Editor Review:", review)

            # 🔥 Detect no improvement
            if prev_issues == review["issues"]:
                print("⚠️ No improvement detected. Stopping early.")
                return writer_output

            if self.should_stop_early(review, i):
                print("✅ Stopping condition met.")
                return writer_output

            prev_issues = review["issues"]
            feedback = review

        return writer_output