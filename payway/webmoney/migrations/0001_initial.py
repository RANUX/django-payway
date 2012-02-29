# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Purse'
        db.create_table('webmoney_purse', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('purse', self.gf('django.db.models.fields.CharField')(unique=True, max_length=13)),
            ('secret_key', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal('webmoney', ['Purse'])

        # Adding model 'ResultResponsePayment'
        db.create_table('webmoney_resultresponsepayment', (
            ('responsepayment_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['accounts.ResponsePayment'], unique=True, primary_key=True)),
            ('LMI_MODE', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('payee_purse', self.gf('django.db.models.fields.related.ForeignKey')(related_name='success_payments', to=orm['webmoney.Purse'])),
            ('LMI_SYS_INVS_NO', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('LMI_SYS_TRANS_NO', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('LMI_SYS_TRANS_DATE', self.gf('django.db.models.fields.DateTimeField')()),
            ('LMI_PAYMENT_NO', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('LMI_PAYER_PURSE', self.gf('django.db.models.fields.CharField')(max_length=13)),
            ('LMI_PAYER_WM', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('LMI_HASH', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('LMI_CAPITALLER_WMID', self.gf('django.db.models.fields.CharField')(max_length=12, blank=True)),
            ('LMI_WMCHECK_NUMBER', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('LMI_PAYMER_NUMBER', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('LMI_PAYMER_EMAIL', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('LMI_TELEPAT_PHONENUMBER', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('LMI_TELEPAT_ORDERID', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('LMI_PAYMENT_DESC', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('LMI_LANG', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
        ))
        db.send_create_signal('webmoney', ['ResultResponsePayment'])

    def backwards(self, orm):
        # Deleting model 'Purse'
        db.delete_table('webmoney_purse')

        # Deleting model 'ResultResponsePayment'
        db.delete_table('webmoney_resultresponsepayment')

    models = {
        'accounts.account': {
            'Meta': {'object_name': 'Account'},
            'currency_code': ('django.db.models.fields.CharField', [], {'default': "'RUB'", 'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uid': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'accounts'", 'to': "orm['auth.User']"})
        },
        'accounts.invoice': {
            'Meta': {'object_name': 'Invoice'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invoices'", 'to': "orm['accounts.Account']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'money_amount': ('django_simptools.money.models.fields.MoneyField', [], {'default': "'0.0'", 'max_digits': '20', 'decimal_places': '2'}),
            'money_amount_currency': ('django_simptools.money.models.fields.CurrencyField', [], {'default': "'XYZ'", 'max_length': '3'}),
            'uid': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True'})
        },
        'accounts.responsepayment': {
            'Meta': {'object_name': 'ResponsePayment'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'accounts_responsepayment_related'", 'to': "orm['accounts.Invoice']"}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'money_amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '2'}),
            'real_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'webmoney.purse': {
            'Meta': {'object_name': 'Purse'},
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'purse': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '13'}),
            'secret_key': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'webmoney.resultresponsepayment': {
            'LMI_CAPITALLER_WMID': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'LMI_HASH': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'LMI_LANG': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'LMI_MODE': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'LMI_PAYER_PURSE': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'LMI_PAYER_WM': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'LMI_PAYMENT_DESC': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'LMI_PAYMENT_NO': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'LMI_PAYMER_EMAIL': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'LMI_PAYMER_NUMBER': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'LMI_SYS_INVS_NO': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'LMI_SYS_TRANS_DATE': ('django.db.models.fields.DateTimeField', [], {}),
            'LMI_SYS_TRANS_NO': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'LMI_TELEPAT_ORDERID': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'LMI_TELEPAT_PHONENUMBER': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'LMI_WMCHECK_NUMBER': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'Meta': {'object_name': 'ResultResponsePayment', '_ormbases': ['accounts.ResponsePayment']},
            'payee_purse': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'success_payments'", 'to': "orm['webmoney.Purse']"}),
            'responsepayment_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['accounts.ResponsePayment']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['webmoney']