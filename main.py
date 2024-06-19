from fastapi import FastAPI

from helpers import log, rate_limiter
from helpers.scheduler import setup as scheduler_setup

# log
log.setup()

# app
app = FastAPI()
rate_limiter.setup(app)

# routes
from helpers import router

router.setup(app)

# scheduler
scheduler_setup(app)

# scheduler jobs
import jobs

_ = jobs.__name__
