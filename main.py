from fastapi import FastAPI

from helpers import cors, log, rate_limiter, static
from helpers.scheduler import setup as scheduler_setup

# log
log.setup()

# app
app = FastAPI()
rate_limiter.setup(app)
cors.setup(app)

# routes
from helpers import router

router.setup(app)
static.setup(app)

# scheduler
scheduler_setup(app)

# scheduler jobs
import jobs

_ = jobs.__name__
