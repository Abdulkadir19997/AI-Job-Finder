#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    #######
    # Apify Tokens initialization
    APIFY_API_TOKEN: Optional[str] = Field(env='APIFY_API_TOKEN')
    ACTOR_TOKEN: Optional[str] = Field(env='ACTOR_TOKEN')

    class Config:
        case_sensitive = True
        env_file = '.env'
        


settings = Settings()
