from types import NoneType
from bs4 import BeautifulSoup, NavigableString, Tag
from click import prompt




class CellcubeXmlElement: 

    def __init__(self, root_tag_name=None, xml=None, features="html.parser"):
        self._root_tag_name = root_tag_name
        self._soup = self._get_soup(xml, features=features)  
        self._tag =  self._soup.find(self._root_tag_name)

    def _get_soup(self, text, features="html.parser") -> BeautifulSoup  :
        soup = BeautifulSoup(text, features=features) 
        return soup

    def root_tag_name(self):
        return self._root_tag_name     

    def set_attribute(self, attribute:str, value:str) :
        if self._tag is not None and attribute is not None:
            if value is not None:
                self._tag[attribute] = value
            else:
                if attribute in self._tag.attrs:
                    del self._tag[attribute]
        return self

    def get_attribute(self, attribute:str, default_value=None) :
        if type(attribute) is str and attribute in self._tag:
            return self._tag[attribute]
        else:
            return default_value

    

    def to_xml(self, beautify=False, indent_level=1):

        if beautify:            
            return  self._tag.prettify()
        return str(self._tag)

    def tag(self):
        return self._tag

    def remove(self):
        if self._tag is not None:           
            self._tag.extract()

    def clear(self):
        if self._tag is not None: 
            self._tag.clear()


    def __str__(self):
        return self.to_xml()


class CellcubeXmlPageLink(CellcubeXmlElement):

    def __init__(self, href=None, content=None, root_tag_name="a", key=None, attributes:dict=dict()):
        CellcubeXmlElement.__init__(self,root_tag_name=root_tag_name, xml=f'<{root_tag_name} href="{href}">{content}</{root_tag_name}>')
        
        self.set_link_content(str(content))
        
        
        if key is not None:        
            attributes["key"]=key

        for key in attributes:
            self.set_link_attribute(key,attributes[key])
        
    def set_link_content(self, content:str):
        self._tag.clear()
        self._tag.append(NavigableString(content if content is not None else ""))
        return self


    def get_link_content(self):
        return self._tag.string
    
    def set_link_attribute(self, attribute:str, value:str) :
        self.set_attribute(attribute=attribute,value=value)
        return self


class CellcubeXmlPageForm(CellcubeXmlElement):

    # self, action:str=None, prompt=str, kind:str=None, var:str=None, attributes:dict=dict(), root_tag_name="form", cellcube_xml_page_form=None, extra=None
    def __init__(self, method="GET", action:str="", prompt=None, kind:str="", var:str="", attributes:dict=dict(), entry_attributes:dict=dict(), root_tag_name="form", cellcube_xml_page_form=None, extra=None):
        #CellcubeXmlElement.__init__(self,root_tag_name=root_tag_name, xml=f'<{root_tag_name} action="{action}"><entry kind="{kind}" var="{var}">{prompt}</entry></{root_tag_name}>')
        CellcubeXmlElement.__init__(self,root_tag_name=root_tag_name, xml=f'<{root_tag_name}><entry></entry></{root_tag_name}>')
        
        #if cellcube_xml_page_form:
        #    self._tag = cellcube_xml_page_form
        self.set_cellcube_xml_page_form(cellcube_xml_page_form)

        self._entry_tag = self._tag.find("entry")
        #self._prompt_tag = self._entry_tag

        if action :        
            attributes["action"]=action

        if method :        
            attributes["method"]=method

        if kind :        
            self.set_kind(kind)
        
        if var :        
            self.set_var(var)

        for key in attributes:
            self.set_form_attribute(key,attributes[key])

        for key in entry_attributes:
            self.set_entry_attribute(key,entry_attributes[key])

        #if prompt:
        #    self._entry_tag.append(prompt)
        
        self.set_prompt(str(prompt))
        
        
    def set_prompt(self, content:str="", prompt_tag_name:str="prompt"):
        if self._entry_tag and self._soup:
            prompt_tag = self._soup.new_tag(prompt_tag_name)
            if content :
                prompt_tag.append(content)
                self._entry_tag.append(prompt_tag)   
                        
        return self
        
    def set_action(self, action:str):
        self.set_attribute('action',action)
        return self

    def set_kind(self, kind:str):
        self.set_entry_attribute('kind',kind)
        return self

    def set_var(self, var:str):
        self.set_entry_attribute('var',var)
        return self


    def get_prompt(self):
        prompt_tag = None        
        if self._entry_tag:
            prompt_tag = self._entry_tag.find("prompt")
        
        
        return prompt_tag.string if prompt_tag else ""


    def _get_attribute(self, attribute_name:str, form_section:str="form", default=None):
        tag = self._tag
        if form_section.lower() == "entry":
            tag = self._entry_tag
        result = None
        try:
            result = tag.attrs[attribute_name]
        except:
            result = default
        return result

    def _set_attribute(self, attribute_name:str, value, form_section:str="form"):
        tag = self._tag       
        
        if form_section.lower() == "entry":
            tag = self._entry_tag
        if tag:
            tag.attrs[attribute_name] = str(value)
        return self

    def get_form_attribute(self, attribute_name:str, default:None):
        # check to see if key exists first
        return self._get_attribute(attribute_name,default=default)

    def get_entry_attribute(self, attribute_name:str, default:None):
        return self._get_attribute(attribute_name,form_section="entry", default=default)
        

    def set_form_attribute(self, attribute_name:str, value):
        return self._set_attribute(attribute_name,value=str(value))

    def set_entry_attribute(self, attribute_name:str, value):
        self._set_attribute(attribute_name,value=str(value), form_section="entry")

    def set_cellcube_xml_page_form(self,cellcube_xml_page_form):
        if cellcube_xml_page_form:
            self._tag = cellcube_xml_page_form


class CellcubeXmlPage(CellcubeXmlElement):

    def __init__(self, default_language:str="en", root_tag_name:str="page", page_tag:str=None, content:str=""):
        CellcubeXmlElement.__init__(self,root_tag_name=root_tag_name, xml=f'<{root_tag_name}></{root_tag_name}>')
        self.default_language = default_language
        if page_tag is not None:
            self.set_page_tag(page_tag)
        content = "" if type(content) is NoneType else content
        self._content = NavigableString(content)
        self._tag.append(self._content)

    

    def parse_from_string(self, xml:str):
        return self

    def set_page_content(self, content:str):
        if content is None: content = ""        
        self._content.extract()
        if ( type(self._content) is NavigableString):
            self._content.extract()
        self._content = NavigableString(content)
        self._tag.insert(0,self._content)
        return self

    def get_page_content(self):        
        return str(self._content)

    def remove_page_content(self):
        if self._content is not None:
            self._content.extract()
        return self

    def get_form(self, form_tag_name:str="form"):
        form_tag = self._tag.find(form_tag_name)
        return form_tag
        #self._form_tag = self._get_soup(f'<{form_tag_name}></{form_tag_name}>').find(form_tag_name)
        
    
    def set_form(self,  form_tag_name:str="form"):
        self._form_tag = self._get_soup(f'<{form_tag_name}></{form_tag_name}>').find(form_tag_name)
        
        if self._content is not None:
            self._tag.insert(1, self._form_tag)
        else:
            self._tag.append(self._form_tag)
        return self

    def remove_form(self):
        if self._form_tag is not None:
            self._form_tag.extract()
        return self
        
    def set_page_attribute(self, attribute:str, value:str) :        
        self.set_attribute(attribute=attribute, value=value)
        return self

    def get_page_attribute(self, attribute:str) -> str :
        if attribute in self.tag().attrs:
            return self.tag().attrs[attribute]
        return None
    
    def set_page_tag(self, tag_name:str):
        self.set_page_attribute("tag",tag_name)
        return self

    def get_page_tag(self):
        return self.get_page_attribute("tag")

    
    def content(self):
        return self._content
        

    def add_content_translation(self, language_code:str, text:str):
        return self

    def add_link(self, link:CellcubeXmlPageLink):
        self._tag.append(link.tag())
        return self

    def add_form(self, form:CellcubeXmlPageForm):
        self._tag.append(form.tag())
        return self

    def remove_link(self, position:int):
        link_to_remove = self.get_link_at(position)
        if link_to_remove is not None:
            link_to_remove.tag().extract()
        return self

    def remove_form(self, position:int):
        form_to_remove = self.get_form_at(position)
        if form_to_remove is not None:
            form_to_remove.tag().extract()
        return self

    def links(self) -> tuple[CellcubeXmlPageLink]:
        result_set = []
        if self._tag:
            links = self._tag.find_all("a")

            for link_tag in links:
                result_set.append(CellcubeXmlPageLink(content=link_tag.string, attributes=link_tag.attrs))
            
        result_set = (result_set)        
        return result_set

    def get_link_at(self, position:int) -> CellcubeXmlPageLink:
        cellcube_xml_page_link = None
        links = self._tag.find_all("a")
        if position < len(links):
            cellcube_xml_page_link = CellcubeXmlPageLink(content=links[position].string, attributes=links[position].attrs)
        return cellcube_xml_page_link

    def get_form_at(self, position:int) -> CellcubeXmlPageForm:
        cellcube_xml_page_form = None
        forms = self._tag.find_all("form")
        if position < len(forms):
            cellcube_xml_page_form = forms[position]
        return cellcube_xml_page_form

    def get_form(self) -> CellcubeXmlPageForm:
        return self.get_form_at(0)
        

    def include_page(self):
        return self


class CellcubeXmlDocument(CellcubeXmlElement):

    def __init__(self, root_tag_name="pages", default_language="en", document_prologue='<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE pages SYSTEM "cellflash-1.3.dtd">', include_prologue=True, xml_input:str=None):
        self.document_prologue = document_prologue
        self.include_prologue = include_prologue
        self.default_language = default_language
        xml = (
        f'{document_prologue}'
        f'<{root_tag_name}>'
        f'</{root_tag_name}>'
        )
        if xml_input is not None: xml = xml_input
        CellcubeXmlElement.__init__(self,root_tag_name=root_tag_name, xml=xml)

    


    def add_single_page(self, page:CellcubeXmlPage=None,  position=None):
        """
        Add new page element to the xml document
        """
        if isinstance(page, CellcubeXmlPage):
            if position is None:
                self._tag.append(page.tag())
            if type(position) is int:
                if position < len(self._tag.contents) and len(self._tag.contents) > 0:
                    self._tag.insert(position, page.tag())
                else:
                    raise Exception(f"Position is out of bound! Value must be below {len(self._tag.contents)}")
        return self   


    def add_multiple_pages(self, pages: list[CellcubeXmlPage]):
        if type(pages) is list:    
            for page in pages:
                self.add_single_page(page)
        return self 


    def get_page_at_position(self, position:int) -> CellcubeXmlPage:
        if type(position) is int:
            if position < len(self._tag.contents) and len(self._tag.contents) > 0:
                page_tag = self._tag.contents[position]
                cellcube_xml_page = self.parse_page_from_tag(page_tag)
                return cellcube_xml_page
            else:
                raise Exception(f"Position is out of bound! Value must be below {len(self._tag.contents)}")


    def get_pages(self) -> tuple[CellcubeXmlPage]:
        results_set = []
        if self._tag:
            all_page_tags = self._tag.find_all("page")
            for page_tag in all_page_tags:                           
                results_set.append(self.parse_page_from_tag(page_tag))
        return (results_set)


    def remove_page_at_position(self, position:int):
        if type(position) is int:
            if position < len(self._tag.contents):
                return self._tag.contents[position].extract()
        return self

    
    def parse_page_from_tag(self, tag:Tag):        
        cellcube_xml_page = CellcubeXmlPage()
        if tag :
            page_content = ""
            # Set page content (text)
            for t in tag.contents:
                if str(t).lower() == "<br/>":
                    page_content += "<br/>"
                else:
                    if type(t) is NavigableString:
                        page_content += t.get_text()
            # Set page content (text)
            cellcube_xml_page.set_page_content(page_content)
            # Set page attributes
            for key in tag.attrs:
                cellcube_xml_page.set_attribute(key,tag.attrs[key] )
            # Set page link
            link_tags = tag.find_all("a")
            for link_tag in link_tags:
                cellcube_xml_page_link = CellcubeXmlPageLink(content=link_tag.string, attributes=link_tag.attrs)
                cellcube_xml_page.add_link(cellcube_xml_page_link)
            # Set page form
            form_tags = tag.find_all("form")
            for form_tag in form_tags:
                entry_tag = form_tag.find("entry")
                prompt_tag = form_tag.find("prompt")                              
                cellcube_xml_page_form = CellcubeXmlPageForm(attributes=form_tag.attrs,entry_attributes=entry_tag.attrs, prompt=prompt_tag.string)
                cellcube_xml_page.add_form(cellcube_xml_page_form)
                
                

        return cellcube_xml_page

    
        

 
        
        
    






