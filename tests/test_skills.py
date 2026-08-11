from agent_core.skills import Skill, SkillRegistry


class A(Skill):
    name = "a"

    def run(self):
        return 1


def test_registry():
    reg = SkillRegistry()
    reg.add(A())
    assert reg.get("a").run() == 1
    assert len(reg.all()) == 1
