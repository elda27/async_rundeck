class Pod(BaseModel):
    value: "Test" = Field(alias='value')


class Test(BaseModel):
    value: Optional["RefTest"] = Field(alias='value')


class RefTest(BaseModel):
    value: Optional[Pod] = Field(alias='value')
