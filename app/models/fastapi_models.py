from pydantic import Field, BaseModel


class SimulationSubmitBody(BaseModel):
    budget: int = Field()
    media: str = Field()


class OptimizationSubmitBody(BaseModel):
    budget: int = Field()
    twitter: bool = Field(default=False)
    youtube: bool = Field(default=False)
    facebook: bool = Field(default=False)
