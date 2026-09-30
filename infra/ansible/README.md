# infra/ansible/

**9. tjedan.** Ansible playbook koji priprema okruženje: instalira potrebne pakete, postavlja konfiguraciju i podiže servise.

Playbook mora biti **idempotentan**: drugo pokretanje ne smije ništa mijenjati (`changed=0`).

```bash
ansible-playbook -i inventory.ini site.yml
```
