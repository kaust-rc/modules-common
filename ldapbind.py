import ldap
import ldap.sasl
import subprocess

ldap.sasl._trace_level = 0
ldap.set_option(ldap.OPT_DEBUG_LEVEL, 0)

class LdapBind:
    def __init__(self):
        self.sasl_auth = ldap.sasl.sasl('', 'GSSAPI')
        self.ldap_connection = ldap.initialize('ldap://wthdc1sr01.kaust.edu.sa', trace_level=0)
        self.ldap_connection.protocol_version = ldap.VERSION3
        self.ldap_connection.set_option(ldap.OPT_REFERRALS, 0)

    def __enter__(self):
        try:
            self._kinit()
            self.ldap_connection.sasl_interactive_bind_s("", self.sasl_auth)
            return self.ldap_connection
        except ldap.LDAPError, e:
            print 'Error using SASL mechanism', self.sasl_auth.mech, str(e)

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.ldap_connection.unbind()
            del self.ldap_connection
        finally:
            self._kdestroy()

    def _kinit(self):
        subprocess.check_call(['kinit', '-t', '/etc/krb5.keytab', '-k', 'host/ubunbtu-14.kaust.edu.sa@KAUST.EDU.SA'])

    def _kdestroy(self):
        subprocess.check_call(['kdestroy'])
