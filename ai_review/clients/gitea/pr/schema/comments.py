from pydantic import BaseModel, RootModel

from ai_review.clients.gitea.pr.schema.user import GiteaUserSchema


class GiteaPRCommentSchema(BaseModel):
    id: int
    user: GiteaUserSchema | None = None
    state: str
    body: str
    commit_id: str | None = None
    stale: bool
    official: bool
    dismissed: bool
    comments_count: int
    submitted_at: str
    updated_at: str
    html_url: str
    pull_request_url: str


class GiteaGetPRCommentsQuerySchema(BaseModel):
    page: int = 1
    per_page: int = 100


class GiteaGetPRCommentsResponseSchema(RootModel[list[GiteaPRCommentSchema]]):
    root: list[GiteaPRCommentSchema]


class GiteaCreateCommentRequestSchema(BaseModel):
    body: str


class GiteaCreateCommentResponseSchema(BaseModel):
    id: int
    body: str
