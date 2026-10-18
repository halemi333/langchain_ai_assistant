
from graph_router import graph


def test_simple_request_uses_normal_route():
    result = graph.invoke({
        "message": "Hello",
        "route": "",
        "response": "",
    })

    assert result["route"] == "normal"
    assert result["response"].startswith("[NORMAL MOCK]")


def test_analysis_keyword_uses_analysis_route():
    result = graph.invoke({
        "message": "Analyze my project",
        "route": "",
        "response": "",
    })

    assert result["route"] == "analysis"
    assert result["response"].startswith("[ANALYSIS MOCK]")


def test_persian_analysis_uses_analysis_route():
    result = graph.invoke({
        "message": "این موضوع را تحلیل کن",
        "route": "",
        "response": "",
    })

    assert result["route"] == "analysis"
    assert result["response"].startswith("[ANALYSIS MOCK]")


if __name__ == "__main__":
    test_simple_request_uses_normal_route()
    test_analysis_keyword_uses_analysis_route()
    test_persian_analysis_uses_analysis_route()

    print("All 3 tests passed!")
