from pipeline.stage import PipelineStage


def test_stage_name_retained() -> None:
    stage = PipelineStage(name="extract")

    assert stage.name == "extract"
