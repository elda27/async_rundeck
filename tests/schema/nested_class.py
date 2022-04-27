class RefTestPre(BaseModel):
    value: Optional[Number] = Field(alias='value')


class Alpha(BaseModel):
    x: Optional[Number] = Field(alias='x')
    y: Optional[Number] = Field(alias='y')


class Beta(BaseModel):
    pre_value: Optional[RefTestPre] = Field(alias='pre_value')
    post_value: Optional["RefTestPost"] = Field(alias='post_value')


class Test(BaseModel):
    alpha: Optional[Alpha] = Field(alias='alpha')
    beta: Optional[Beta] = Field(alias='beta')


class RefTestPost(BaseModel):
    value: Optional[Number] = Field(alias='value')
