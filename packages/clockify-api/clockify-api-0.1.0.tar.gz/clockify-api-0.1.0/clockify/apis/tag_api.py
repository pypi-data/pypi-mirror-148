from typing import List
from clockify.config import BASE_URL
from clockify.model.tag_model import Tag
from clockify.wrapper import Wrapper


class TagWrapper(Wrapper):
    def get_tags(self, workspace_id: str) -> List[Tag]:
        url = self.__url(workspace_id)
        return self.get_list(url, Tag)

    def get_tag(self, workspace_id: str, tag_id: str) -> Tag:
        url = self.__url(workspace_id, tag_id)
        return self.get_one(url, Tag)

    def create_tag(self, tag: Tag) -> Tag:
        url = self.__url(tag.workspace_id)
        return self.create_one(url, tag, Tag)

    def delete_tag(self, workspace_id: str, tag_id: str) -> Tag:
        url = self.__url(workspace_id, tag_id)
        return self.delete_one(url, Tag)

    def update_tag(self, tag: Tag) -> Tag:
        url = self.__url(tag.workspace_id, tag.id_)
        return self.update_one(url, tag, Tag)

    def __url(self, workspace_id: str, tag_id: str = None) -> str:
        url = f"{BASE_URL}/workspaces/{workspace_id}/tags"
        if tag_id:
            url += f"/{tag_id}"
        return url
