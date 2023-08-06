import json
import random
import uuid
from dataclasses import dataclass, field
from hashlib import sha256
from datetime import datetime
import couchdb2
from  . import exceptions
__version__ = "0.4.0"


def make_id(json: str) -> str:
    return sha256(bytes(json, encoding="utf-8")).hexdigest()


@dataclass
class BookerDocument:
    """Class for Documents to be stored in Booker
    If the Document is labeled private then
    the meta data will be labled private and will
    not be gloably searched."""

    is_public: bool
    operation_id: int = field(kw_only=True, init=True, default=0)
    _id: str = field(kw_only=True, default=None)
    _rev: str = field(kw_only=True, default=None)
    _attachments: dict = field(default_factory=dict, kw_only=True)
    owner_id: int = field(kw_only=True, default=0)
    document_id: str = field(kw_only=True, default="")
    type: str = field(kw_only=True, default="")
    source_dataset: str = field(default="Star Intel", kw_only=True)
    dataset: str = field(default="Star Intel", kw_only=True)
    date_added: str = field(default=datetime.now().isoformat(), kw_only=True)
    date_updated: str = field(default=datetime.now().isoformat(), kw_only=True)
    doc: dict = field(default_factory=dict, kw_only=True)

    def parse_doc(self, doc):
        self.doc = json.loads(doc)
        if self.doc.get("_id", None) is not None:
            self._id = self.doc["_id"]
        if self.doc.get("_rev", None) is not None:
            self._rev = self.doc["_rev"]
        if self.doc.get("_attachments", None) is not None:
            self._attachments = self.doc["_attachments"]


@dataclass
class BookerPerson(BookerDocument):
    fname: str = field(kw_only=True, default="")
    lname: str = field(kw_only=True, default="")
    mname: str = field(default="", kw_only=True)
    bio: str = field(default="", kw_only=True)
    age: int = field(default=0, kw_only=True)
    dob: str = field(default="", kw_only=True)
    social_media: list[str] = field(default_factory=list, kw_only=True)
    phones: list[str] = field(default_factory=list, kw_only=True)
    address: list[str] = field(default_factory=list, kw_only=True)
    ip: list[str] = field(default_factory=list, kw_only=True)
    data_breach: list[str] = field(default_factory=list, kw_only=True)
    emails: list[str] = field(default_factory=list, kw_only=True)
    organizations: list[str] = field(default_factory=list, kw_only=True)
    memberships: list[str] = field(default_factory=list, kw_only=True)
    education: list[dict] = field(default_factory=list, kw_only=True)
    comments: list[dict] = field(default_factory=list, kw_only=True)
    type = "person"

    def make_doc(self, use_json=False):

        metadata = {
            "fname": self.fname,
            "mname": self.mname,
            "lname": self.lname,
            "age": self.age,
            "dob": self.dob,
            "emails": self.emails,
            "phones": self.phones,
            "ip": self.ip,
            "orgs": self.organizations,
            "comments": self.comments,
            "bio": self.bio,
            "locations": self.address,
            "social_media": self.social_media,
            "education": self.education,
            "memberships": self.memberships
        }

        if self.is_public:
            doc = {
                "operation_id": self.operation_id,
                "type": "person",
                "date_added": self.date_added,
                "date_updated": self.date_updated,
                "dataset": self.dataset,
                "source_dataset": self.source_dataset,
                "metadata": metadata,
                "owner_id": self.owner_id
            }

        else:
            doc = {
                "operation_id": self.operation_id,
                "type": "person",
                "date_added": self.date_added,
                "date_updated": self.date_updated,
                "dataset": self.dataset,
                "source_dataset": self.source_dataset,
                "private_metadata": metadata,
                "owner_id": self.owner_id
            }
        if self._id:
            doc["_id"] = self._id
        if self._rev:
            doc["_rev"] = self._rev
        if use_json:
            return json.dumps(doc)
        else:
            return doc

    def load(self, doc):
        if doc.get("type") == "person":
            meta = get_meta(doc)
            self._id = doc.get("_id")
            self._rev = doc.get("_rev")
            self.date_added = doc.get("date_added")
            self.date_updated = doc.get("date_updated")
            self.source_dataset = doc.get("source_dataset")
            self.dataset = doc.get("dataset")
            self.owner_id = doc.get("owner_id")

            self.fname = meta["fname"]
            self.mname = meta["mname"]
            self.lname = meta["lname"]
            self.age = meta["age"]
            self.dob = meta["dob"]
            self.organizations = meta.get("orgs")
            self.address = meta.get("locations")
            self.comments = meta.get("comments")
            self.bio = meta.get("bio")
            self.emails = meta.get("emails")
            self.social_media = meta.get("social_media")
            self.ip = meta.get("ip")
            self.phones = meta.get("phones")
            self.memberships = meta.get("memberships")

        return self
    def resolve(self, client):
        """For each remote document load and build a BookerDocument"""
        resolved_emails = []
        resolved_phones = []
        resolved_orgs = []
        resolved_social_media = []
        resolved_ip = []
        resolved_memberships = []
        ids = []
        ids = ids.extend(self.organizations)
        ids = ids.extend(self.emails)
        ids = ids.extend(self.address)
        ids = ids.extend(self.phones)
        ids = ids.extend(self.ip)
        ids = ids.extend(self.social_media)
        ids = ids.extend(self.memberships)
        docs = client.get_bulk(ids)

        for doc_ in docs:
            if doc_ is not None:
                try:
                    dtype = doc_['type']
                    if dtype == "email":
                        resolved_emails.append(BookerEmail().load(doc_))
                    elif dtype == "org":
                        resolved_orgs.append(BookerOganizations().load(doc_))
                    elif dtype == "phone":
                        resolved_phones.append(BookerPhone().load(doc_))
                    elif dtype == "username":
                        resolved_social_media.append(BookerUsername().load(doc_))
                    elif dtype == "membership":
                        resolved_memberships.append(BookerMembership().load(doc_))
                except KeyError:
                    raise exceptions.TypeMissingError()





@dataclass
class BookerOganizations(BookerDocument):
    name: str = field(kw_only=True, default="")

    country: str = field(default="")
    bio: str = field(default="")
    organization_type: str = field(kw_only=True, default="NGO")
    reg_number: str = field(kw_only=True, default="")
    members: list[dict] = field(default_factory=list)
    address: list[dict] = field(default_factory=list)
    email_formats: list[str] = field(default_factory=list)
    type = "org"

    def make_doc(self, use_json=False):
        metadata = {
            "name": self.name,
            "country": self.country,
            "members": self.members,
            "address": self.address,
            "reg_number": self.reg_number,
            "org_type": self.organization_type,
            "email_formats": self.email_formats,
        }
        if self.is_public:
            doc = {
                "operation_id": self.operation_id,
                "type": "org",
                "date_added": self.date_added,
                "date_updated": self.date_updated,
                "dataset": self.dataset,
                "source_dataset": self.source_dataset,
                "metadata": metadata,
                "owner_id": self.owner_id
            }
        else:
            doc = {
                "operation_id": self.operation_id,
                "type": "org",
                "date_added": self.date_added,
                "date_updated": self.date_updated,
                "dataset": self.dataset,
                "source_dataset": self.source_dataset,
                "private_metadata": metadata,
                "owner_id": self.owner_id
            }
        if use_json:
            return json.dumps(doc)
        else:
            return doc

    def load(self, doc):
        if doc.get("type") == "org":
            meta = get_meta(doc)
            self._id = doc.get("_id")
            self._rev = doc.get("_rev")
            self.date_added = doc.get("date_added")
            self.date_updated = doc.get("date_updated")
            self.source_dataset = doc.get("source_dataset")
            self.dataset = doc.get("dataset")
            self.owner_id = doc.get("owner_id")

            self.name = meta.get("name")
            self.country = meta.get("country")
            self.bio = meta.get("bio")
            self.organization_type = meta.get("org_type")
            self.members = meta.get("members")
            self.reg_number = meta.get("reg_number")
            self.address = meta.get("address")
            self.email_formats = meta.get("address")

        return self


@dataclass
class BookerEmail(BookerDocument):
    owner: str = field(kw_only=True)
    email_username: str = field(kw_only=True, default="")
    email_domain: str = field(kw_only=True, default="")
    email_password: str = field(kw_only=True, default="")
    data_breach: list[string] = field(default_factory=list, kw_only=True)
    username: dict = field(kw_only=True, default_factory=dict)
    type = "email"

    def make_doc(self, use_json=False):
        metadata = {
            "owner": self.owner,
            "email_username": self.email_username,
            "username": self.username,
            "email_domain": self.email_domain
        }
        if self.is_public:
            doc = {
                "operation_id": self.operation_id,
                "type": "email",
                "date_added": self.date_added,
                "date_updated": self.date_updated,
                "dataset": self.dataset,
                "source_dataset": self.source_dataset,
                "metadata": metadata,
                "owner_id": self.owner_id
            }
        else:
            doc = {
                "operation_id": self.operation_id,
                "type": "email",
                "date_added": self.date_added,
                "date_updated": self.date_updated,
                "dataset": self.dataset,
                "source_dataset": self.source_dataset,
                "private_metadata": metadata,
                "owner_id": self.owner_id
            }
        if self._id:
            doc["_id"] = self._id
        if self._rev:
            doc["_rev"] = self._rev

        if use_json:
            return json.dumps(doc)
        else:
            return doc

    def load(self, doc):
        if doc.get("type") == "email":
            meta = get_meta(doc)
            self._id = doc.get("_id")
            self._rev = doc.get("_rev")
            self.date_added = doc.get("date_added")
            self.date_updated = doc.get("date_updated")
            self.source_dataset = doc.get("source_dataset")
            self.dataset = doc.get("dataset")
            self.owner_id = doc.get("owner_id")

            self.email_domain = meta.get("email_domain")
            self.email_username = meta.get("email_username")
            self.username = meta.get("username")
            self.email_password = meta.get("email_password")
            self.owner = meta.get("owner")
            self.date_seen = meta.get("date_seen")
            self.data_breach = meta.get("data_breach")
        return self

    def make_resolve(self):
        """Builds a dict for a resolve result"""
        data = {}
        data["email"] = self.email_username + "@" + self.email_domain
        data["password"] = self.email_password
        data["data_breaches"] = []
        for breach in self.data_breach:
            data["data_breaches"].append(breach)
        data["owner"] = self.owner
        return data

@dataclass
class BookerBreach(BookerDocument):
    date: str
    total: int
    description: str
    url: str
    type = "breach"

    def make_doc(self, use_json=False):
        metadata = {
            "date": self.date,
            "total": self.total,
            "description": self.description,
            "url": self.url,
        }
        if self.is_public:
            doc = {
                "operation_id": self.operation_id,
                "type": "breach",
                "date_added": self.date_added,
                "date_updated": self.date_updated,
                "dataset": self.dataset,
                "source_dataset": self.source_dataset,
                "metadata": metadata,
                "owner_id": self.owner_id
            }
        else:
            doc = {
                "operation_id": self.operation_id,
                "type": "breach",
                "date_added": self.date_added,
                "date_updated": self.date_updated,
                "dataset": self.dataset,
                "source_dataset": self.source_dataset,
                "private_metadata": metadata,
                "owner_id": self.owner_id
            }
        if self._id:
            doc["_id"] = self._id
        if self._rev:
            doc["_rev"] = self._rev

        if use_json:
            return json.dumps(doc)
        else:
            return doc

    def load(self, doc):
        if doc.get("type") == "breach":
            meta = get_meta(doc)
            self._id = doc.get("_id")
            self._rev = doc.get("_rev")
            self.date_added = doc.get("date_added")
            self.date_updated = doc.get("date_updated")
            self.source_dataset = doc.get("source_dataset")
            self.dataset = doc.get("dataset")
            self.owner_id = doc.get("owner_id")
            self.date = meta.get("date")
            self.total = meta.get("total")
            self.description = meta.get("description")
            self.url = meta.get("url")
        return self


@dataclass
class BookerWebService(BookerDocument):
    port: int
    service_name: str
    service_version: str
    source: str
    ip: str
    owner: str
    type = "service"

    def make_doc(self, use_json=False):
        metadata = {
            "port": self.port,
            "ip": self.ip,
            "name": self.service,
            "source": self.source,
            "date": self.date,
            "version": self.end_date,
            "owner": self.owner
        }
        if self.is_public:
            doc = {
                "operation_id": self.operation_id,
                "type": "web_service",
                "date_added": self.date_added,
                "date_updated": self.date_updated,
                "source_dataset": self.source_dataset,
                "dataset": self.dataset,
                "metadata": metadata,
                "owner_id": self.owner_id
            }
        else:
            doc = {
                "operation_id": self.operation_id,
                "type": "web_service",
                "date_added": self.date_added,
                "date_updated": self.date_updated,
                "source_dataset": self.source_dataset,
                "dataset": self.dataset,
                "private_metadata": metadata,
                "owner_id": self.owner_id
            }

        if self._id:
            doc["_id"] = self._id
        if self._rev:
            doc["_rev"] = self._rev

        if use_json:
            return json.dumps(doc)
        else:
            return doc
    def load(self, doc):
        if doc.get("type") == "service":
            meta = get_meta(doc)
            self._id = doc.get("_id")
            self._rev = doc.get("_rev")
            self.date_added = doc.get("date_added")
            self.date_updated = doc.get("date_updated")
            self.source_dataset = doc.get("source_dataset")
            self.dataset = doc.get("dataset")
            self.owner_id = doc.get("owner_id")
            self.port = meta.get("port")
            self.ip = meta.get("ip")
            self.service_version = meta.get("version")
            self.service_name = meta.get("name")
        return self


@dataclass
class BookerHost(BookerDocument):
    ip: str
    hostname: str
    operating_system: str
    date: str
    asn: int = field(kw_only=True, default=0)
    country: str = field(kw_only=True, default="")
    network_name: str = field(kw_only=True, default="")
    owner: str = field(kw_only=True, default="")
    vulns: list[dict] = field(default_factory=list)
    services: list[dict] = field(default_factory=list)
    type = "host"

    def make_doc(self, use_json=False):
        metadata = {
            "ip": self.ip,
            "hostname": self.hostname,
            "asn": self.asn,
            "owner": self.owner,
            "network_name": self.network_name,
            "country": self.country,
            "os": self.operating_system,
            "vulns": self.vulns,
            "services": self.services,
        }
        if self.is_public:
            doc = {
                "operation_id": self.operation_id,
                "type": "host",
                "date_added": self.date_added,
                "date_updated": self.date_updated,
                "source_dataset": self.source_dataset,
                "dataset": self.dataset,
                "metadata": metadata,
                "owner_id": self.owner_id
            }
        else:
            doc = {
                "operation_id": self.operation_id,
                "type": "host",
                "date_added": self.date_added,
                "date_updated": self.date_updated,
                "dataset": self.dataset,
                "source_dataset": self.source_dataset,
                "private_metadata": metadata,
                "owner_id": self.owner_id
            }
        if self._id:
            doc["_id"] = self._id
        if self._rev:
            doc["_rev"] = self._rev

        if use_json:
            return json.dumps(doc)
        else:
            return doc

    def load(self, doc):
        if doc.get("type") == "host":
            meta = get_meta(doc)
            self._id = doc.get("_id")
            self._rev = doc.get("_rev")
            self.date_added = doc.get("date_added")
            self.date_updated = doc.get("date_updated")
            self.source_dataset = doc.get("source_dataset")
            self.dataset = doc.get("dataset")
            self.owner_id = doc.get("owner_id")
            self.services = doc.get("services")
            self.hostname = doc.get("hostname")
            self.asn = doc.get("asn")
            self.owner = doc.get("owner")
            self.network_name = doc.get("network_name")
            self.operating_system = doc.get("os")
            self.vulns = doc.get("vulns")
            self.country = doc.get("country")
        return self

@dataclass
class BookerCVE(BookerDocument):
    cve_number: str
    score: int
    type = "cve"
    def make_doc(self, use_json=False):
        metadata = {
            "cve_number": cve_number,
            "score": self.score,
        }
        if self.is_public:
            doc = {
                "type": "cve",
                "date_added": self.date_added,
                "date_updated": self.date_updated,
                "dataset": self.dataset,
                "source_dataset": self.source_dataset,
                "metadata": metadata,
                "owner_id": self.owner_id
            }
        else:
            doc = {
                "type": "cve",
                "date_added": self.date_added,
                "date_updated": self.date_updated,
                "dataset": self.dataset,
                "source_dataset": self.source_dataset,
                "private_metadata": metadata,
                "owner_id": self.owner_id
            }

        if self._id:
            doc["_id"] = self._id
        if self._rev:
            doc["_rev"] = self._rev

        if use_json:
            return json.dumps(doc)
        else:
            return doc
    def load(self, doc):
        if doc.get("type") == "cve":
            meta = get_meta(doc)
            self._id = doc.get("_id")
            self._rev = doc.get("_rev")
            self.date_added = doc.get("date_added")
            self.date_updated = doc.get("date_updated")
            self.source_dataset = doc.get("source_dataset")
            self.dataset = doc.get("dataset")
            self.owner_id = doc.get("owner_id")
            self.cve_number = doc.get("cve_number")
            self.score = doc.get("score")


@dataclass
class BookerMesaage(BookerDocument):
    platform: str  # Domain of platform aka telegram.org. discord.gg
    media: bool
    username: str = field(kw_only=True)
    fname: str = field(kw_only=True, default="")
    lname: str = field(kw_only=True, default="")
    phone: str = field(kw_only=True)  # Used for signal and telegram
    user_id: str = field(
        kw_only=True, default=""
    )  # Hash the userid of the platform to keep it uniform
    # Should be a hash of groupname, message, date and username.
    # Using this system we can track message replys across platforms amd keeps it easy
    message_id: str = field(kw_only=True)
    group_name: str = field(kw_only=True)  # Server name if discord
    channel_name: str = field(kw_only=True)  # only used incase like discord
    message: str = field(kw_only=True)
    message_type: str = field(kw_only=True)  # type of message
    is_reply: bool = field(kw_only=True)
    reply_id: str = field(kw_only=True, default="")

    def make_doc(self, use_json=False):
        metadata = {
            "platform": self.platform,
            "date": self.date,
            "is_reply": self.is_reply,
            "username": self.username,
            "message": self.message,
            "message_type": self.message_type,
            "user_id": self.user_id,
            "message_id": self.message_id,
            "date": self.date_added,
            "is_media": self.media,
            "fname": self.fname,
            "lname": self.lname,
        }
        if self.is_public:
            doc = {
                "operation_id": self.operation_id,
                "type": "message",
                "dataset": self.dataset,
                "date_added": self.date_added,
                "date_updated": self.date_updated,
                "source_dataset": self.source_dataset,
                "metadata": metadata,
                "owner_id": self.owner_id
            }
        else:
            doc = {
                "operation_id": self.operation_id,
                "type": "message",
                "dataset": self.dataset,
                "date_added": self.date_added,
                "date_updated": self.date_updated,
                "source_dataset": self.source_dataset,
                "private_metadata": metadata,
                "owner_id": self.owner_id
            }

        if self._id:
            doc["_id"] = self._id
        if self._rev:
            doc["_rev"] = self._rev

        if use_json:
            return json.dumps(doc)
        else:
            return doc

        def load(self, doc):
            meta = get_meta(doc)
            self._id = doc.get("_id")
            self._rev = doc.get("_rev")
            self.date_added = doc.get("date_added")
            self.date_updated = doc.get("date_updated")
            self.source_dataset = doc.get("source_dataset")
            self.dataset = doc.get("dataset")
            self.owner_id = doc.get("owner_id")
            self.fname = doc.get("fname")
            self.lname = doc.get("lname")


@dataclass
class BookerAddress(BookerDocument):
    street: str = field(kw_only=True, default="")
    city: str = field(kw_only=True, default="")
    state: str = field(kw_only=True, default="")
    apt: str = field(kw_only=True, default="")
    zip: str = field(kw_only=True, default="")
    members: list = field(kw_only=True, default_factory=list)
    type = "address"

    def make_doc(self, use_json=False):
        metadata = {
            "street": self.street,
            "apt": self.apt,
            "zip": self.zip,
            "state": self.state,
            "city": self.city,
            "members": self.members,
        }
        if self.is_public:
            doc = {
                "operation_id": self.operation_id,
                "type": "address",
                "dataset": self.dataset,
                "source_dataset": self.source_dataset,
                "metadata": metadata,
                "owner_id": self.owner_id
            }
        else:
            doc = {
                "operation_id": self.operation_id,
                "type": "adress",
                "dataset": self.dataset,
                "source_dataset": self.source_dataset,
                "private_metadata": metadata,
                "owner_id": self.owner_id
            }

        if self._id:
            doc["_id"] = self._id
        if self._rev:
            doc["_rev"] = self._rev

        if use_json:
            return json.dumps(doc)
        else:
            return doc

    def load(self, doc):
        if doc.get("type") == "address":
            meta = doc.get("metadata")
            if meta is None:
                meta = doc.get("private_metadata")
            self.street = meta.get("street")
            self.city = meta.get("city")
            self.state = meta.get("state")
            self.apt = meta.get("apt")
            self.zip = meta.get("zip")
            self.members = meta.get("members")
            self._id = doc.get("_id")
            self._rev = doc.get("_rev")
            self.date_added = doc.get("date_added")
            self.date_updated = doc.get("date_updated")
            self.source_dataset = doc.get("source_dataset")
            self.dataset = doc.get("dataset")
            self.owner_id = doc.get("owner_id")

        return self


@dataclass
class BookerUsername(BookerDocument):
    username: str
    platform: str
    owner: str = field(kw_only=True, default="")
    email: str = field(kw_only=True, default="")
    phone: str = field(kw_only=True, default="")
    orgs: list[string] = field(kw_only=True, default_factory=list)
    type = username
    def make_doc(self, use_json=False):
        metadata = {
            "username": self.username,
            "platform": self.platform,
            "owner": self.owner,
            "email": self.email,
            "phone": self.phone,
            "membership": self.org,
        }
        if self.is_public:
            doc = {
                "operation_id": self.operation_id,
                "type": "username",
                "dataset": self.dataset,
                "source_dataset": self.source_dataset,
                "metadata": metadata,
                "owner_id": self.owner_id
            }
        else:
            doc = {
                "operation_id": self.operation_id,
                "type": "username",
                "dataset": self.dataset,
                "source_dataset": self.source_dataset,
                "private_metadata": metadata,
                "owner_id": self.owner_id
            }
        if self._id:
            doc["_id"] = self._id
        if self._rev:
            doc["_rev"] = self._rev

        if use_json:
            return json.dumps(doc)
        else:
            return doc
    def load(self, doc):
        meta = get_meta(doc)
        self._id = doc.get("_id")
        self._rev = doc.get("_rev")
        self.date_added = doc.get("date_added")
        self.date_updated = doc.get("date_updated")
        self.source_dataset = doc.get("source_dataset")
        self.dataset = doc.get("dataset")
        self.owner_id = doc.get("owner_id")
        try:
            self.username = meta["username"]
            self.platform = meta["platform"]
            self.email = meta["email"]
        except KeyError:
            raise exceptions.DocumentParseError()


@dataclass
class BookerPhone(BookerDocument):
    owner:  str = field(kw_only=True, default="")
    phone: str = field(kw_only=True, default="")
    carrier: str = field(kw_only=True, default="")
    status: str = field(kw_only=True, default="N/A")

    def make_doc(self, use_json=False):
        metadata = {
            "owner": self.owner,
            "phone": self.phone,
            "carrier": self.carrier,
        }
        if self.is_public:
            doc = {
                "operation_id": self.operation_id,
                "type": "username",
                "dataset": self.dataset,
                "source_dataset": self.source_dataset,
                "metadata": metadata,
                "owner_id": self.owner_id
            }
        else:
            doc = {
                "operation_id": self.operation_id,
                "type": "username",
                "dataset": self.dataset,
                "source_dataset": self.source_dataset,
                "private_metadata": metadata,
                "owner_id": self.owner_id
            }
        if self._id:
            doc["_id"] = self._id
        if self._rev:
            doc["_rev"] = self._rev

        if use_json:
            return json.dumps(doc)
        else:
            return doc


    def load(self, doc):
        meta = get_meta(doc)
        self._id = doc.get("_id")
        self._rev = doc.get("_rev")
        self.date_added = doc.get("date_added")
        self.date_updated = doc.get("date_updated")
        self.source_dataset = doc.get("source_dataset")
        self.dataset = doc.get("dataset")
        self.owner_id = doc.get("owner_id")

        try:
            self.phone = meta.get("phone")
            self.carrier = meta.get("carrier")
            self.owner = meta.get("owner")
        except KeyError:
            raise exceptions.ParseDocumentError()

@dataclass
class BookerMembership(BookerDocument):
    """This Document type is used for tracking memberships"""
    type = "membership"
    start_date:  str = field(kw_only=True, default="")
    end_date:  str = field(kw_only=True, default="")
    roles: list = field(kw_only=True, default_factory=list())
    title:  str = field(kw_only=True, default="")

    def load(self, doc):
        meta = get_meta(doc)
        self._id = doc.get("_id")
        self._rev = doc.get("_rev")
        self.date_added = doc.get("date_added")
        self.date_updated = doc.get("date_updated")
        self.source_dataset = doc.get("source_dataset")
        self.dataset = doc.get("dataset")
        self.owner_id = doc.get("owner_id")

        try:
            self.start_date = meta.get("start_date")
            self.end_date = meta.get("end_date")
            self.roles = meta.get("roles")
            self.title = meta.get("title")
        except KeyError:
            raise exceptions.ParseDocumentError

    def make_doc(self, use_json=False):
        metadata = {
            "start_date": self.start_date,
            "end_date": self.end_date,
            "roles": self.roles,
            "title": self.title
        }
        if self.is_public:
            doc = {
                "operation_id": self.operation_id,
                "type": "membership",
                "dataset": self.dataset,
                "source_dataset": self.source_dataset,
                "metadata": metadata,
                "owner_id": self.owner_id
            }
        else:
            doc = {
                "operation_id": self.operation_id,
                "type": "membership",
                "dataset": self.dataset,
                "source_dataset": self.source_dataset,
                "private_metadata": metadata,
                "owner_id": self.owner_id
            }
        if self._id:
            doc["_id"] = self._id
        if self._rev:
            doc["_rev"] = self._rev

        if use_json:
            return json.dumps(doc)
        else:
            return doc


def get_meta(doc):
    """Load the documunt metadata field wether it is private or not"""
    meta = doc.get("metadata")
    if meta is None:
        meta = doc.get("private_metadata")

    # if meta is still None the type field is not set.
    if meta is None:
        raise exceptions.TypeMissingError()
    else:
        return meta

def load_doc(client, doc):
    """Load a document. it will determin the type then load it."""
    obj = None
    if doc is not None:
        type = doc.get("type")
        if type is None:
            raise exceptions.TypeMissingError()
        else:
            if type == "person":
                obj = BookerMember().load(doc)
            elif type == "org":
                obj = BookerOrganization().load(doc)
            elif type == "email":
                obj = BookerEmail().load(doc)
            elif type == "address":
                obj = BookerAddress().load(doc)
        if obj is None:
            raise exceptions.DocumentParseError("Failed to load document becuase a type could not be matched")
        else:
            return obj
