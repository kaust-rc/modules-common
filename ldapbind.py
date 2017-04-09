import subprocess
import ldap
import ldap.sasl


class LdapBind(object):
    def __init__(self):
        self.sasl_auth = ldap.sasl.sasl('', 'GSSAPI')
        self.ldap_connection = ldap.initialize('ldap://wthdc1sr01.kaust.edu.sa', trace_level=0)
        self.ldap_connection.protocol_version = ldap.VERSION3
        self.ldap_connection.set_option(ldap.OPT_REFERRALS, 0)

    def __enter__(self):
        try:
            LdapBind.kinit()
            self.ldap_connection.sasl_interactive_bind_s("", self.sasl_auth)
            return self.ldap_connection
        except ldap.LDAPError, error:
            print 'Error using SASL mechanism', self.sasl_auth.mech, str(error)

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.ldap_connection.unbind()
            del self.ldap_connection
        finally:
            LdapBind.kdestroy()

    @staticmethod
    def kinit():
        subprocess.check_call(['kinit', '-t', '/etc/krb5.keytab', '-k', 'host/ubunbtu-14.kaust.edu.sa@KAUST.EDU.SA'])

    @staticmethod
    def kdestroy():
        subprocess.check_call(['kdestroy'])
