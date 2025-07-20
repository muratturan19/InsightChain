from backend.agents.reporter_agent import generate_report

if __name__ == "__main__":
    sample_json = '{"company_summary": "Test", "decision_makers": []}'
    html = generate_report(sample_json, tool_mode=True)
    print(html[:200])  # print first 200 chars
