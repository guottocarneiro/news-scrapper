from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama


class ArticleProcessor:
    def __init__(self, model_name="deepseek-r1:14b"):
        self.llm = ChatOllama(model=model_name)

        self.summary_prompt = PromptTemplate(
            input_variables=["content"],
            template="Resuma o seguinte artigo:\n\n{content}\n\nResumo:",
        )

        self.entities_prompt = PromptTemplate(
            input_variables=["content"],
            template="Liste as entidades nomeadas encontradas no seguinte artigo:\n\n{content}\n\nEntidades:",
        )

        self.output_parser = StrOutputParser()

        self.summary_chain = self.summary_prompt | self.llm | self.output_parser
        self.entities_chain = self.entities_prompt | self.llm | self.output_parser

    def process_article(self, article: dict) -> dict:
        content = article.get("content", "")
        summary = self.summary_chain.invoke({"content": content})
        entities = self.entities_chain.invoke({"content": content})
        return {
            "title": article.get("title", ""),
            "summary": summary,
            "entities": entities,
        }
