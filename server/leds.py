# Make a single thread worker that processes updates to the LEDs.
# Write an async function that schedules work to be done in the worker.
# This is not a queue: only the most recent unpainted update is kept.
# TODO: add a FPS counter somewhere, and count the number of dropped frames.

