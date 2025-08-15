from fastapi import FastAPI

from helpers import cors, error_handler, log, rate_limiter, static
from helpers.lifespan import lifespan

# log
log.setup()

# app
app = FastAPI(lifespan=lifespan)
error_handler.setup(app)
rate_limiter.setup(app)
cors.setup(app)

# routes
from helpers import router

router.setup(app)
static.setup(app)

# scheduler jobs
import jobs

_ = jobs.__name__
