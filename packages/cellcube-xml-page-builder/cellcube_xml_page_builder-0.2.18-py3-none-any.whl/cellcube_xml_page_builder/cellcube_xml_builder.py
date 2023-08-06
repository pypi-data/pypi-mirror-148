

from .cellcube_xml_elements import CellcubeXmlDocument, CellcubeXmlElement, CellcubeXmlPage, CellcubeXmlPageLink, CellcubeXmlPageForm
 

class Part():

    def __init__(self, attributes:dict=dict(), root_tag_name:str="element", features="html.parser", extra=None):
        self._root_tag_name=root_tag_name
        self._cellcube_xml_element = CellcubeXmlElement(root_tag_name=root_tag_name, features=features)
        self.extra = extra # Some extra value
        for key in attributes:
            self._cellcube_xml_element.set_attribute(attribute=key, value=attributes[key])

    def _set_attribute(self, name:str, value):
        self._cellcube_xml_element.set_attribute(attribute=name,value=value)
        return self

    def _get_attribute(self, name:str, default=None):
        return self._cellcube_xml_element.get_attribute(name,default_value=default)        

    def xml(self, beautify:bool=False, indent_level=1):
        result =  self._cellcube_xml_element.to_xml(beautify=beautify, indent_level=indent_level) if self._cellcube_xml_element is not None else f"<{self._root_tag_name}></{self._root_tag_name}>"
        return result

    def get_attributes(self):
        return self.cellcube_xml_element_tag().attrs

    def cellcube_xml_element(self):
        return self._cellcube_xml_element 

    def cellcube_xml_element_tag(self):
        return self._cellcube_xml_element.tag() if self._cellcube_xml_element is not None else None

    def __str__(self):
        return self.xml()

    

    
class Link(Part):
    def __init__(self, href:str=None, text=str, key:str=None, attributes:dict=dict(), root_tag_name="a", cellcube_xml_page_link:CellcubeXmlPageLink=None, extra=None):
        self._attributes = attributes
        self._root_tag_name=root_tag_name
        self._cellcube_xml_element = CellcubeXmlPageLink(href=href, key=key, content=text, root_tag_name=self._root_tag_name, attributes=attributes)
        self.text = text
        self.key = key
        self.href = href          
        self.set_cellcube_xml_page_link(cellcube_xml_page_link)

    def set_link_text(self, text:str):
        self.text = text
        self._cellcube_xml_element.set
        return self

    def get_link_text(self) -> str:
        return self._cellcube_xml_element.get_link_content()

    def set_link_destination(self, url:str):
        self.set_link_attribute("href",url)
        return self

    def get_link_destination(self) -> str:
        return self.get_link_attribute("href",'')

    def set_link_attribute(self, attribute_name:str, attribute_value): 
        if (str(attribute_name).lower() == "href"):
            self.href = attribute_value      
        if (str(attribute_name).lower() == "key"):
            self.key = attribute_value    
        
        self.cellcube_xml_element_tag().attrs[attribute_name] = attribute_value# ((name=attribute_name,default=default)     
        #self._set_attribute(name=attribute_name,value=attribute_value)
        return self

    def get_link_attribute(self, attribute_name:str, default=None): 
        try:
            return self.cellcube_xml_element_tag().attrs[attribute_name]
        except:
            return default      
        #return self._get_attribute(name=attribute_name,default=default)

    def set_cellcube_xml_page_link(self, cellcube_xml_page_link:CellcubeXmlPageLink):
        if cellcube_xml_page_link is not None:
            self._cellcube_xml_element = cellcube_xml_page_link
        return self
        
    

class Form(Part):

    def __init__(self, method="GET", action:str=None, prompt:str=None, kind:str=None, var:str=None, attributes:dict=dict(), root_tag_name="form", cellcube_xml_page_form:CellcubeXmlPageForm=None, extra=None):
        self._attributes = attributes
        self._root_tag_name=root_tag_name
        self._cellcube_xml_element = CellcubeXmlPageForm(action=action, prompt=prompt, kind=kind, var=var, root_tag_name=self._root_tag_name, attributes=attributes, cellcube_xml_page_form=cellcube_xml_page_form)
        self.prompt = self.set_prompt(prompt)
        self.method = method
        self.action = action
        self.kind = kind    
        self.var = var       
        #self.set_cellcube_xml_page_form(cellcube_xml_page_form)

    def set_prompt(self, text:str):
        self._cellcube_xml_element.set_prompt(text)
        return self

    def set_action(self, action:str):
        self._cellcube_xml_element.set_attribute("action",action)
        return self

    def set_method(self, method:str):
        self._cellcube_xml_element.set_attribute("method", str(method).upper())
        return self

    def set_kind(self, kind:str):
        self._cellcube_xml_element.set_entry_attribute("kind", kind)
        return self

    def set_var_name(self, var_name:str):
        self._cellcube_xml_element.set_entry_attribute("var", var_name)
        return self


    def get_prompt(self):
        return self._cellcube_xml_element.get_prompt()

    def get_action(self, default=None):
        return self._cellcube_xml_element.get_form_attribute("action", default=default)

    def get_method(self, default="GET"):
        return self._cellcube_xml_element.get_form_attribute("method", default=default)

    def get_kind(self, default=None):
        return self._cellcube_xml_element.get_entry_attribute("kind", default=default)

    def get_var_name(self, default=None):
        return self._cellcube_xml_element.get_entry_attribute("var", default=default)



    

    def set_cellcube_xml_page_form(self, cellcube_xml_page_form:CellcubeXmlPageForm):
        if cellcube_xml_page_form is not None:
            self._cellcube_xml_element = cellcube_xml_page_form
        return self
    pass

class Page(Part):

    def __init__(self, content:str=None, tag:str=None, form:Form=None, links:list[Link]=(), attributes:dict=dict(), default_language="en", root_tag_name="page", cellcube_xml_page:CellcubeXmlPage=None):
        
        self._attributes = attributes
        
        self._root_tag_name=root_tag_name
        self._cellcube_xml_element = CellcubeXmlPage(default_language=default_language, page_tag=tag, content=content, root_tag_name=self._root_tag_name)
        self.content = content
        
        self.set_page_text(content)
        #self.links_ = links
        self.form = form
        self.tag = tag
        
        # Set page attributes
        for key in attributes:
            self._attributes[key]=attributes[key]

        # Set page form
        if form:
            self.set_form(form)

        # Set page links
        for link in links:
            self.add_link(link=link)

        self.set_cellcube_xml_page(cellcube_xml_page)

    @property
    def text(self):
        return self.get_page_text()

    @text.setter
    def temperature(self, value):
        self.set_page_text(value)

    def set_cellcube_xml_page(self, cellcube_xml_page:CellcubeXmlPage):
        if cellcube_xml_page is not None:
            self._cellcube_xml_element = cellcube_xml_page
        return self

    def set_page_attribute(self, attribute_name:str, attribute_value):        
        #self._set_attribute(name=attribute_name,value=attribute_value)
        self.cellcube_xml_element_tag().attrs[attribute_name] = attribute_value
        return self

    def get_page_attribute(self, attribute_name:str, default=None):
        #self._get_attribute(attribute_name=attribute_name,default=default)
        try:
            return self.cellcube_xml_element_tag().attrs[attribute_name]
        except:
            return default

    def set_tag(self, tag:str):
        self.set_page_attribute(name="tag",value=tag)
        return self

    def get_tag(self):
        return self.get_page_attribute("tag")

    def set_descr(self, descr:str):
        self._set_attribute(name="descr",value=descr)
        return self

    def get_descr(self):
        return self._get_attribute("descr")

    def set_page_text(self, text:str):
        self._cellcube_xml_element.set_page_content(content=text)
        self.content=text
        return self

    def get_page_text(self) -> str:   
        return self._cellcube_xml_element.get_page_content() 

    def clear_page_text(self):
        self._cellcube_xml_element.remove_page_content()
        self.content=None
        return self

    def set_form(self, form:Form):
        if form:
            cellcube_xml_page_form = CellcubeXmlPageForm(action=form.get_action()
            , prompt=form.get_prompt()
            , kind=form.get_kind()
            , var=form.get_var_name()
            , attributes=form.get_attributes())
            self._cellcube_xml_element.add_form(cellcube_xml_page_form)
        return self

    def get_form(self)->Form:        
        cellcube_xml_page_form=self._cellcube_xml_element.get_form()        
        if cellcube_xml_page_form:
            return Form(cellcube_xml_page_form=self._cellcube_xml_element.get_form())
        else:
            return None
        


    def add_link(self, link:Link):
        self._cellcube_xml_element.add_link(link.cellcube_xml_element())
        return self
        
    def get_link_at_index(self, index:int):
        # A implémenter
        try:
            return self.links_[index]
        except:
            pass
        return self

    def remove_link_at_index(self, index:int):
        self._cellcube_xml_element.remove_link(index)
        return self


    def links(self) -> tuple[Link]:        
        """Return links"""
        # Get all page tags
        links = []
        cellcube_xml_page_links = self._cellcube_xml_element.links()
        for cellcube_xml_page_link in cellcube_xml_page_links:
            links.append(Link(cellcube_xml_page_link=cellcube_xml_page_link))
        return (links)




    def __str__(self) -> str:
        return super().__str__()


class Document(Part):
    
    def __init__(self, page:Page=None, pages:list[Page]=[], attributes:dict=dict(), default_language="en", root_tag_name="pages", document_prologue='<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE pages SYSTEM "cellflash-1.3.dtd">', include_prologue=True, xml_input:str=None, include_default_page=True):
        self._attributes = attributes
        self._root_tag_name=root_tag_name
        self._cellcube_xml_element = CellcubeXmlDocument(root_tag_name=self._root_tag_name, default_language=default_language, document_prologue=document_prologue, include_prologue=include_prologue, xml_input=xml_input)
        
        if xml_input is not None:
            for key in attributes:
                self._set_attribute(key, attributes[key])

        if page:            
            self.add_page(page=page)

        

    def add_pages(self, *args):
        for arg in args: 
            if type(arg) is str:
                self.add_page(content=arg)
            if (type(arg) is Page):
                self.add_page(page=arg)
        return self


    def add_page(self, content:str=None, page:Page=None, position=None):
        if content is not None and page is None:
            page = Page(content=content)
        self._cellcube_xml_element.add_single_page(page.cellcube_xml_element(),position=position)       
        return self

    def get_page_at_index(self, index:int) -> Page:  
        cellcube_xml_page = self._cellcube_xml_element.get_page_at_position(index)  
        page = Page(cellcube_xml_page=cellcube_xml_page)        
        return page
        

    def remove_page_at_index(self, index:int):
        self._cellcube_xml_element.remove_page_at_position(position=index)    
        return self

    def pages(self) -> tuple[Page]:        
        """Return pages"""
        # Get all page tags
        pages = []
        cellcube_xml_pages = self._cellcube_xml_element.get_pages()
        for cellcube_xml_page in cellcube_xml_pages:            
            pages.append(Page(cellcube_xml_page=cellcube_xml_page))
        return (pages)

    def xml(self, beautify=False, indent_level=1) -> str:
        xml = Part.xml(self,beautify=beautify,indent_level=indent_level)
        #xml = self._cellcube_xml_element.tag() if self._cellcube_xml_element is not None else ""
        if self._cellcube_xml_element.include_prologue:
            if beautify is True:
                xml = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE pages SYSTEM "cellflash-1.3.dtd">\n' + xml
            else:
                xml = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE pages SYSTEM "cellflash-1.3.dtd">' + xml
        
        return xml
        #return self._cellcube_xml_element.tag() if self._cellcube_xml_element is not None else None


class CellcubeXmlPageBuilder:

    def __init__(self):
        pass

    
    def build_xml_page(self, content:str="", page_tag:str=None, root_tag_name:str="page", default_language:str="en", links:list[Link]=[], attributes:dict=dict(), as_document:bool=False, beautify=False) -> str:
        
        xml_document = Document(page=Page(
            content=content
            , tag=page_tag
            , default_language=default_language
            , root_tag_name=root_tag_name
            , links=links
            , attributes=attributes
        ))

        
        return xml_document.xml(beautify=beautify) if not as_document  else xml_document

    def build_xml_form_page(self):
        pass

    def new_cellecube_xml_document(self, page:Page=None, pages:list[Page]=[], attributes:dict=dict(), default_language="en", root_tag_name="pages", document_prologue='<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE pages SYSTEM "cellflash-1.3.dtd">', include_prologue=True):
        return Document(page=page, pages=pages, attributes=attributes, default_language=default_language, root_tag_name=root_tag_name, document_prologue=document_prologue, include_prologue=include_prologue)

    def parse_xml_document(self, string:str) -> Document:
        return Document(xml_input=string)

