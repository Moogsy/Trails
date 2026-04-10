from workers import app


@app.task(name="workers.tasks.session_winddown")
def session_winddown(session_id: str) -> None:
    # Notify users session is ending soon
    raise NotImplementedError


@app.task(name="workers.tasks.session_ceiling")
def session_ceiling(session_id: str) -> None:
    # Hard-end the session
    raise NotImplementedError


@app.task(name="workers.tasks.consistency_decay")
def consistency_decay(answer_id: str) -> None:
    # Decay consistency score 7 days after answer submitted
    raise NotImplementedError


@app.task(name="workers.tasks.run_match_batch")
def run_match_batch() -> None:
    from matching.batch import run_batch
    run_batch()
