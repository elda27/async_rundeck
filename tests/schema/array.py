class TestRequired(BaseModel):
    value: List["RefTest"] = Field(alias='value')


class Test(BaseModel):
    value: Optional[List["RefTest"]] = Field(alias='value')


class RefTest(BaseModel):
    value: Optional["Pod"] = Field(alias='value')
